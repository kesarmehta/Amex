import openai

# Set your OpenAI API key
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key

def generate_response(prompt, text_input):
    try:
        # Call the GPT-3 API to generate a response
        response = openai.Completion.create(
            engine="davinci",  # Use the "davinci" engine (or other available engines)
            prompt=f"{prompt}\nInput: {text_input}\nOutput:",
            max_tokens=50,  # Adjust this based on the desired response length
        )

        # Extract and return the generated text
        generated_text = response.choices[0].text
        return generated_text

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    # User inputs
    prompt = "Translate the following English text to French:"
    text_input = "Hello, how are you?"

    # Generate the response
    generated_output = generate_response(prompt, text_input)

    # Print the generated output
    print("Generated Output:", generated_output)
