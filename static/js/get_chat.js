








$(document).ready(function () {



function fetchChatHistory() {
    $.ajax({
        url: "/get_chats",
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.chats.length === 0) {
                $("#chat-box").hide(); // Hide chat box if no messages
                return;
            }

            $("#chat-box").empty().show(); // Show chat box if messages exist

            data.chats.forEach(chat => {
                let userMessage = `<div class="mb-4 p-3 rounded-lg bg-[#444654] text-white text-right">${chat.user_message}</div>`;
                
                let botMessage = "";
                if (chat.bot_type === "text") {
                    botMessage = `<div class="mb-4 p-3 rounded-lg text-white text-left">${chat.bot_message}</div>`;
                } else if (chat.bot_type === "image_url") {
                    botMessage = `<div class="mb-4 p-3 rounded-lg text-white text-left"><img src="${chat.bot_message}" class="max-w-xs rounded-lg shadow-md" /></div>`;
                }

                $("#chat-box").append(userMessage + botMessage);
            });

            // Auto-scroll to the latest message
            $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
        },
        error: function () {
            console.error("❌ Failed to fetch chat history");
        }
    });
}



fetchChatHistory(); 


});