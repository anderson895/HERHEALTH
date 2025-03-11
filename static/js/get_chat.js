








$(document).ready(function () {

    var target_date = $("#target_date").val();


    console.log(target_date);

    function fetchChatHistory() {
        $.ajax({
            url: "/get_chats",
            type: "GET",
            data: { "target_date": target_date },
            dataType: "json",
            success: function (data) {
                if (!data.chats || data.chats.length === 0) {
                    $("#chat-box").hide();
                    return;
                }
    
                $("#chat-box").empty().show();
    
                data.chats.forEach(chat => {
                    let userMessage = `<div class="mb-4 p-3 rounded-lg bg-[#444654] text-white text-right">${chat.user_message}</div>`;
                    
                    let botMessage = "";
                    if (chat.bot_type === "text") {
                        botMessage = `<div class="mb-4 p-3 rounded-lg text-white text-left">${chat.bot_message}</div>`;
                    } else if (chat.bot_type === "img_url") {
                        botMessage = `<img src="${chat.bot_message}" class="w-full mt-2" alt="Bot Image" />`;
                    }
    
                    $("#chat-box").append(userMessage + botMessage);
                });
    
                // Only auto-scroll if the user is already at the bottom
                let chatBox = $("#chat-box");
                let isScrolledToBottom = chatBox.scrollTop() + chatBox.innerHeight() >= chatBox[0].scrollHeight - 10;
    
                if (isScrolledToBottom) {
                    chatBox.scrollTop(chatBox[0].scrollHeight);
                }
            },
            error: function (xhr, status, error) {
                console.error("❌ Failed to fetch chat history:", error);
                alert("Failed to load chat history. Please try again.");
            }
        });
    }
    



fetchChatHistory(); 


});