import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = "protonx-models/protonx-legal-tc"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

examples = [
    "3. Chöng chi dinh mo màng phôi",
        "Khōng có chōng chì dinh tuyēt dōi cho mò màng phōi ngoai trù truòng hop nguài bēnh có",
        "bēnh ly làm phōi dính hoàn toàn vào thành ngurc, màng phōi vách hoá nhiēu.",
        "Chöng chi dinh tuong dōi trong các truòng hgp: Bēnh nhān có nguy co cháy máu do",
        "rōi loan dōng máu, dang dùng thuōc chōng dōng. Các truròng hgp này có thé tiēn hành thú",
        "thuāt khi d truyēn dù cá yēu tō dōng máu và tiēu cāu dē dám báo ò mú nguy cō cháy",
        "máu thäp trò lēn (Tiéu cau > 60G/L và ApT bēnh/chúng < 1.5)."
]

for text in examples:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            num_beams=10,
            max_new_tokens=32,
            length_penalty=1.0,
            early_stopping=True,
            repetition_penalty=1.2,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"Input:  {text}")
    print(f"Output: {result}")
    print("-" * 30)
