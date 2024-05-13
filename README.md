```
# PDFGPT

PDFGPT is a web application built with React and Flask that leverages the power of OpenAI's GPT-3.5 model to generate text summaries and responses based on input PDF documents. It utilizes various technologies and libraries including Langchain, FAISS, OpenAI embedding, and GPT-3.5 turbo model.

## Features

- Summarize PDF documents using advanced natural language processing techniques.
- Generate responses and answers based on the content of PDF documents.
- Utilizes Langchain for language processing tasks.
- Incorporates FAISS for efficient similarity search.
- Harnesses the power of OpenAI embedding and GPT-3.5 turbo model for generating high-quality text.
- Frontend built with React, TypeScript, Tailwind CSS, and DaisyUI for a modern and responsive user interface.

## Installation

To run PDFGPT locally, follow these steps:

1. Clone the repository:
   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```
   cd PDFGPT
   ```

3. Install dependencies for the frontend:
   ```
   cd frontend
   npm install
   ```

4. Install dependencies for the backend:
   ```
   cd ../backend
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Create a `.env` file in the `backend` directory.
   - Add your GPT-3.5 API key to the `.env` file:
     ```
     OPENAI_API_KEY=<your_openai_api_key>
     ```


6. Run the backend:
   ```
   flask run
   ```

7. Run the frontend:
   ```
   npm start
   ```

8. Access the application in your browser at `http://localhost:3000`.

## Usage

- Upload a PDF document using the provided interface.
- Choose from various options such as summarization or response generation.
- View the generated output based on the selected task.

## Contributing

Contributions to PDFGPT are welcome! If you have any ideas for improvements, new features, or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

PDFGPT was made possible thanks to the following technologies and libraries:

- React
- Flask
- OpenAI GPT-3.5
- Langchain
- FAISS
- Tailwind CSS
- DaisyUI
- TypeScript

## Contact

For any inquiries or feedback, please contact (mail to:gang.expert.99@gmail.com).
```

Feel free to customize the content as needed for your project!
