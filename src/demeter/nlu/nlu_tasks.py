import os
from transformers import BertTokenizer
import tensorflow as tf
from tensorflow import keras
from nlu.enums import Intent, Slot


class NLUTasks:

    def __init__(self, model_path, params_path, model_name = "bert-base-multilingual-cased"):
        self.model_path = model_path
        self.model_name = model_name

        # Load model
        self.model = tf.saved_model.load(self.model_path)
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)

        # Load Intents
        with open(os.path.join(params_path,"intents.txt") , 'r') as file_params:
            self.intent_names = file_params.read().split("\n")
        self.intent_map = dict((label, idx) for idx, label in enumerate(self.intent_names))

        # Load Slots
        with open(os.path.join(params_path,"slots.txt") , 'r') as file_params:
            self.slot_names = file_params.read().split("\n")
        self.slot_map = {}
        for label in self.slot_names:
            self.slot_map[label] = len(self.slot_map)

    def _decode_predictions(self, text, intent_id, slot_ids):
        info = {"intent": intent_id, "name" : self.intent_names[intent_id]}
        collected_slots = {}
        active_slot_words = []
        active_slot_name = None
        for word in text.split():
            tokens = self.tokenizer.tokenize(word)
            current_word_slot_ids = slot_ids[:len(tokens)]
            slot_ids = slot_ids[len(tokens):]
            current_word_slot_name = self.slot_names[current_word_slot_ids[0]]
            if current_word_slot_name == "O":
                if active_slot_name:
                    collected_slots[active_slot_name] = " ".join(active_slot_words)
                    active_slot_words = []
                    active_slot_name = None
            else:
                # Naive BIO: handling: treat B- and I- the same...
                new_slot_name = current_word_slot_name[2:]
                if active_slot_name is None:
                    active_slot_words.append(word)
                    active_slot_name = new_slot_name
                elif new_slot_name == active_slot_name:
                    active_slot_words.append(word)
                else:
                    collected_slots[active_slot_name] = " ".join(active_slot_words)
                    active_slot_words = [word]
                    active_slot_name = new_slot_name
        if active_slot_name:
            collected_slots[active_slot_name] = " ".join(active_slot_words)
        info["slots"] = collected_slots
        return info

    def nlu(self, text):
        inputs = tf.constant(self.tokenizer.encode(text))[None, :]  # batch_size = 1
        outputs = self.model(inputs)
        slot_logits, intent_logits = outputs
        slot_ids = slot_logits.numpy().argmax(axis=-1)[0, 1:-1]
        intent_id = intent_logits.numpy().argmax(axis=-1)[0]
        return self._decode_predictions(text, intent_id, slot_ids)

