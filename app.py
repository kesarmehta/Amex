# app.py
from flask import Flask, render_template, request
import openai
import PyPDF2

app = Flask(__name__)

# Set your OpenAI API key
api_key = "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"


openai.api_key = api_key


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":

        source = request.form.get("text_input")

        # Check if a file was submitted
        if "pdf_file" in request.files:
            pdf_file = request.files["pdf_file"]
            if pdf_file.filename != "":
                # Read the PDF file and extract text
                pdf_text = extract_text_from_pdf(pdf_file)

                
                # Define your prompt
                prompt=f"Analyze the policy's impact on {source} ( and describe how it affects it breifly in bullet points (if it doesnt impact return DOES NOT IMPACT). \n\n Here is the content of the policy: \n\n{pdf_text}"
                #prompt = f"Analyze the policy's impact on {source} and provide a detailed description of how it affects them. Please be thorough in your response. Here is the content of the policy:\n\n{pdf_text}"
                

                # Call the GPT-3 API with an increased max_tokens value
                response = get_completion(prompt)
                print(response)

                # Extract and store the generated text
                result = response


    return render_template('index.html', result=result)



def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    
    return response.choices[0].message["content"]


def extract_text_from_pdf(pdf_file):
    try:
        # Initialize a PDF file reader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the extracted text
        pdf_text = ""

        # Loop through each page of the PDF and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

        # Close the PDF file
        pdf_file.close()

        # Return the extracted text as a string
        return pdf_text
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)




from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Example data, replace this with your API's output
    bullet_points = [
        "The policy allows for prompt payment of pension to retired government employees, including basic pension and increased Dearness Relief (DR), without the need for forwarding government orders to the bank.",
        "Agency banks are instructed to follow all guidelines and instructions from the government promptly, without waiting for further instructions from RBI.",
        "The policy aims to provide expeditious service to senior citizens and reduce the time lag between issuing DR orders and payment to beneficiaries.",
        "The policy does not impact the return of HDFC Bank."
    ]

    return render_template('index.html', bullet_points=bullet_points)

if __name__ == "__main__":
    app.run(debug=True)
