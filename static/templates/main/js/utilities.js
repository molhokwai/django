
function extractAndRemoveThinkTag(text){
    // Define the regex pattern to match <think>(.*)</think>
    const regex = /<think>(.*?)<\/think>/s;

    // Extract the value inside the <think> tags
    const match = regex.exec(text);
    const extractedThinkValue = match ? match[1] : null;

    // Remove the matched pattern from the text
    const cleanedResponseText = text.replace(regex, '');

    return {
        extractedThinkValue,
        cleanedResponseText,
    };
}


// Function to decode Unicode escape sequences
function decodeUnicode(str) {
    return str.replace(/\\u[\dA-F]{4}/gi, 
        match => String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16))
    );
}
