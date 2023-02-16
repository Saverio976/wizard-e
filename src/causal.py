from transformers import BloomTokenizerFast 
from petals import DistributedBloomForCausalLM

MODEL_NAME = "bigscience/bloom-petals"
tokenizer = BloomTokenizerFast.from_pretrained(MODEL_NAME)
model = DistributedBloomForCausalLM.from_pretrained(MODEL_NAME)
model = model.cuda()

sess = model.inference_session(max_length=512)

PREFIX = None

def get_response(text: str) -> str:
    global PREFIX
    res = ""
    if PREFIX is None:
        PREFIX = f"Human: {text}\nFriendly AI:"
    PREFIX = tokenizer(PREFIX, return_tensors="pt")["input_ids"].cuda()
    bot_respond = True
    while bot_respond:
        outputs = model.generate(
            PREFIX, max_new_tokens=1, do_sample=True, top_p=0.9, temperature=0.75, session=sess
        )
        outputs = tokenizer.decode(outputs[0, -1:])
        res += outputs
        if "\n" in outputs:
            bot_respond = False
        PREFIX = None
    return res

def end_session():
    sess.close()
