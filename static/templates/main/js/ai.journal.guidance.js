
let promptInput;
let chatContainer;
let chatContainerWaitText;

let chatId;
let chatIdIntval;
let chatAddHistory;

let feedbackTextEl;

document.addEventListener('DOMContentLoaded', function(event){

    // Set elements
    promptInput = document.getElementById('prompt-input');
    chatContainer = document.getElementById('chat-container');
    feedbackTextEl = document.querySelector("#chat-container .feedback");
    chatContainerWaitText = document.querySelector('#chat-container .wait.text');
    chatAddHistory = document.querySelector('#chatPromptAndResponseAddHistory');

    // JavaScript to handle sending messages and displaying responses
    document.getElementById('send-button').addEventListener('click', function() {
        clearFeedbacks()

        chatContainerWaitText.style.opacity = 1;
        promptInput.classList.add("wait");
        promptInput.disabled = true;

        const userMessage = promptInput.value.trim();

        // -----------
        //    PROMPT
        //      Set chatPromptAndResponseId check first...
        // -----------
        chatIdIntval = setInterval(() => {
            chatId = 
                document.getElementById(
                        "chatPromptAndResponseId").value;

            console.log(`chatPromptAndResponseId: ${chatId}`);

            if(chatId){
                clearInterval(chatIdIntval);
            }

        }, 2000);

        promptLLM(
            userMessage,
            saveLLMResponse,
            handleLLMError
        );

        try{
            if(chatContainerJsUpdate){
                // JS update deactivated by default..

                // Get the user's message
                if (userMessage === '') return;

                // Display the user's message
                const userMessageElement = document.createElement('div');
                userMessageElement.className = 'message user-message';
                userMessageElement.textContent = `You: ${userMessage}`;
                chatContainer.appendChild(userMessageElement);

                // Clear the input
                promptInput.value = '';

                // Simulate a bot response (replace with actual API call)
                setTimeout(() => {
                    const botMessage = `Bot: You said "${userMessage}"`;
                    const botMessageElement = document.createElement('div');
                    botMessageElement.className = 'message bot-message';
                    botMessageElement.textContent = botMessage;
                    chatContainer.appendChild(botMessageElement);

                    // Scroll to the bottom of the chat container
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }, 1000);        
            }

        } catch(e){
            console.log('chat container js update error :: Missing global variable `chatContainerJsUpdate` ?');            
        }
    });

    // Allow pressing Enter to send the message
    // !Cancelled, not good UIP
    // -------------------------
    document.getElementById('prompt-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            // !Cancelled
            // ----------
            document.getElementById('send-button').click();
        }
    });
});


function clearFeedbacks(){
    chatContainerWaitText.style.opacity = 0;
    feedbackTextEl.textContent = "";
}    


function onPromptRespondedTo(){
    promptInput.value = "";
    promptInput.classList.remove("wait");
    promptInput.disabled = false;
    if(chatAddHistory.checked){ chatAddHistory.click(); }
    chatContainerWaitText.style.opacity = 0;
    feedbackTextEl.textContent = "";
}    


function promptLLM(question, successCallback, errorCallback){
    /**************
     * Sample response:
     *  {"model":"deepseek-r1:1.5b","created_at":"2025-02-12T14:04:29.802546912Z","response":"\u003cthink\u003e\n\n\u003c/think\u003e\n\nHi! I'm DeepSeek-R1, an AI assistant independently developed. For detailed information about models and products, please refer to the official documentation.","done":true,"done_reason":"stop","context":[151644,17360,2385,84,650,444,10994,17607,151645,151648,271,151649,271,13048,0,358,2776,18183,39350,10911,16,11,458,15235,17847,28135,7881,13,1752,11682,1995,911,4119,323,3871,11,4486,8300,311,279,3946,9705,13],"total_duration":3601564510,"load_duration":18680838,"prompt_eval_count":10,"prompt_eval_duration":526000000,"eval_count":35,"eval_duration":3055000000}
     **************/ 

    let chatHistory = '';
    if(chatAddHistory && chatAddHistory.checked){
        Unicorn.call('chat.chat_prompt', 'get_history');
        chatHistory = Unicorn.getReturnValue('chat.chat_prompt');
    }
    question = `${question}\n\n\n${chatHistory}`;


    if(question.indexOf('##Test:') == 0){
        let f = null;
        if(question.indexOf('##Test:OK') == 0){

            const thinkText = "<think>Think test value...</think>\n\n";
            const response = `${thinkText}You sent: ${question}`

            f = () => { successCallback(response); };
            
        } else if(question.indexOf('##Test:Error') == 0){

            f = () => { errorCallback('The application', `You sent: ${question}`); };
            
        }
        // simulate long query and return...
        setTimeout(f, 5000);
        return
    }

    console.log(`------------| Prompt Ollama - Question: ${question}`);

    // Replace with your Ollama server URL
    const ollamaServerUrl = 'http://217.154.4.222:11434/api/generate';

    fetch(ollamaServerUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: question, model:"deepseek-r1:1.5b",stream:false })
    })
    .then(response => response.json())
    .then(data => {
        const responseTextContent = data.response || null;
        successCallback(responseTextContent);
    })
    .catch(error => {
        console.error('Error:', error);
        const responseTextContent = 'Failed to get a response from the server.';
        errorCallback('Ollama', error);
    });
}

function saveLLMResponse(response){
    /****************
     * 
     * success:
     *      1-   extract <think> value from response text
     *      2-   clean text
     *      3-   Set response and <think> text to current ChatPromptResponse
     *           front object values:
     *           !! The values are data bound (no defer) so corresponding 
     *              ChatPromptResponse is immediately updated 
     *      4-   Call chat_prompt Unicorn view Unicorn view to update and reload
     *          => Use current ChatPromptResponse object
     *             Use #chatPromptAndResponseId value if there, else:
     *             Must set id of last prompt in hidden "last_prompt_id"
     * 
     *****************/

    //* success:
    //*      0-   call the method for all the prompt responded
    //*           to actions...
    //*      1-   extract <think> value from response text
    //*      2-   clean text
    //* -------

    //*      0-   call the method for all the prompt responded
    //*           to actions...
    onPromptRespondedTo();

    //*      1-   extract <think> value from response text
    //*      2-   clean text
    //* -------
    const responseText = decodeUnicode(response);

    const result = extractAndRemoveThinkTag(responseText);
    let extractedThinkValue = result.extractedThinkValue;
    let cleanedResponseText = result.cleanedResponseText;

    console.log("Extracted Value:", extractedThinkValue);
    console.log("Cleaned Text:", cleanedResponseText);    

    //*      3-   Set response and <think> text to current ChatPromptResponse
    //*           ! Data immediately saved
    //*             ... see details in functions' description...
    //* -------
    document.getElementById(
        'chatPromptAndResponseResponse').value = cleanedResponseText;
    document.getElementById(
        'chatPromptAndResponseThink').value = extractedThinkValue;

    //*      4-   Call chat_prompt Unicorn view to update and reload
    const _response = cleanedResponseText;
    const think = extractedThinkValue;

    //* Convert object to query string
    const params = { _response, think };
    const queryString = new URLSearchParams(params).toString();

    Unicorn.call( 
        'chat.chat_prompt', 'update_prompt',
        queryString
    );
}


function handleLLMError(src, error){
    /****************
     * 
     * error:
     *    display in "#chat-container .feedback"
     *      -   set text
     *      -   add error class: "error-message"
     *      -   set timeout to remove text and error class...
     * 
     *****************/
    const errorMsg = `${src} Error: "${error}"`;
    console.log(errorMsg);

    feedbackTextEl.textContent = `${src} returned and error. Hover on this messsage to read it...`;
    feedbackTextEl.classList.add("error-message");
    feedbackTextEl.title = errorMsg;

    if(false){
        // No timeout, message stays until next execution...         
        setTimeout(() => {
            feedbackTextEl.textContent = "";
            feedbackTextEl.classList.remove("error-message");
        }, 10000)
    }
}

