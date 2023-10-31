$(document).ready(function () {
    $("#initial-message").hide();
    $("#chat").append("<div class='message stark' id='typing-blob'><div class='typing typing-1'></div><div class='typing typing-2'></div><div class='typing typing-3'></div></div>").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)
    setTimeout(function () {
        $("#typing-blob").remove();
        $("#initial-message").show();
    }, 5000);
});

var datetime;
var sound = new Audio();
sound.src = 'https://www.zapsplat.com/wp-content/uploads/2015/sound-effects-35448/zapsplat_cartoon_bubble_pop_003_40275.mp3';


var ws;
var wsUri = "ws:";
var loc = window.location;
var responseMessage = {};
console.log(loc);
if (loc.protocol === "https:") { wsUri = "wss:"; }

wsUri += "//" + loc.host + loc.pathname.replace("test", "ws/test");

function wsConnect() {
    console.log("connect", wsUri);
    ws = new WebSocket("wss://devapi.orca.embiote.in/ws/simple");

    ws.onmessage = function (msg) {
        var line = "";

        var data = JSON.parse(msg.data);
        responseMessage["context"] = data["context"];
        console.log(msg);
        line += "<p>" + data.text + "</p>";

        $("#typing-blob").remove()
        $("#chat").append("<div class='message stark back'>" + line + "</div>").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)
        var newPageTitle = data.text;
        document.title = "Bot reply: " + newPageTitle;
        if (data.options !== null) {
            $("#Query").prop("disabled", true);
            $("#chat").append("<div class='message stark' id='typing-blob'><div class='typing typing-1'></div><div class='typing typing-2'></div><div class='typing typing-3'></div></div>").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)
            setTimeout(function () {
                $("#typing-blob").remove()
            }, 1290);
            setTimeout(() => {
                $(document).ready(function () {
                    for (let i = 0; i < data.options[0].length; i++) {
                        if (data.options[0][i].text !== undefined) {
                            $("#chat").append("<button class='message stark extra' data-value=\"" + data.options[0][i].text + "\" onclick='myFun(this)'> <span>" + data.options[0][i].text + "</span></button>").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)
                        }
                    }
                })
            }, 1300);
        } else {
            $("#Query").prop("disabled", false);
        }
        timing();
        $("#chat").append(`<div class='bot-timer' id='time'>Today at ${datetime} </div>`).animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)

    }

    ws.onopen = function () {
        console.log("connected");
    }
    ws.onclose = function () {
        setTimeout(wsConnect, 3000);
    }
}

function doit(m) {
    if (ws) { ws.send(m); }
}
function openChatBox() {
    $("#chatBox").removeClass("closed")
    $("#closeButton").show();

    $("#online-status").attr("class", "online-status");

}
function closeChatBox() {
    $("#chatBox").addClass("closed")
    $("#closeButton").hide();
    emojifn(this);

}

function timing() {
    var currentdate = new Date();
    var hrs = currentdate.getHours();
    console.log(hrs);
    console.log(typeof (hrs));
    var day;
    if (hrs > 12) {
        hrs = hrs - 12;
        console.log(hrs);
        day = "PM";

    }
    else {
        day = "AM";
    }

    datetime = + hrs + ":"
        + currentdate.getMinutes() + " " + day;
    console.log(datetime);
};

function sendMessage(userResponse) {
    if (userResponse !== "") {
        responseMessage["text"] = userResponse
        doit(JSON.stringify(responseMessage));
        responseMessage = {};
        $("#chat").append("<div class='message parker'>" + userResponse + "</div>").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)
        timing();
        $("#chat").append(`<div class='timer' id='time'>Today at ${datetime} </div>`).animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)
        sound.play();
        $("#chat").append("<div class='message stark' id='typing-blob'><div class='typing typing-1'></div><div class='typing typing-2'></div><div class='typing typing-3'></div></div>").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 500)
        $("#Query").val("");
        setTimeout(function () {
            $("#typing-blob").remove()
        }, 5000);
        document

    }
}

function sendFromTextBox() {
    var userResponse = $("#Query").val();
    // console.log(userResponse);
    sendMessage(userResponse);
    userResponse = "";
    document.getElementById('micIcon').className = "fas fa-microphone";

}

function myFun(btn) {
    console.log(btn.dataset.value);
    userResponse = btn.dataset.value;
    sendMessage(userResponse);
}

$(document).ready(function () {
    $("#closeButton").hide();
    setTimeout(function () {
        $("#chatBox").removeClass("closed");
        $("#closeButton").show();
    }, 0);
    document.getElementById('micIcon').className = "fas fa-microphone";

});


function record() {
    $(document).ready(function () {
        $('input[name="msg-txt"]').attr('placeholder', 'Listening.....');
    })
    setTimeout(() => {
        $(document).ready(function () {
            $('input[name="msg-txt"]').attr('placeholder', 'Type your message here!');
        })
    }, 4000);
    var recognition = new webkitSpeechRecognition();
    recognition.lang = "";
    recognition.onresult = function (event) {
        console.log(event);
        document.getElementById('Query').value = event.results[0][0].transcript;
        setTimeout(() => {
            var userResponse = $("#Query").val();
            console.log(userResponse);

            sendMessage(userResponse);
            userResponse = "";
        }, 2000);

        $(document).ready(function () {
            $('input[name="msg-txt"]').attr('placeholder', 'Type your message here!');
        })


    }
    recognition.start();
}
function iconFunction() {
    if (document.getElementById('micIcon').className == "fas fa-microphone") {
        record();
    }
    if (document.getElementById('micIcon').className == "fas fa-paper-plane") {
        sendFromTextBox();
    }


}

var emojisTitles = [['😄'], ['😁'], ['😆'], ['😅 ',], ['🤣'], ['😂'], ['🙂'], ['🙃'], ['😉'], ['😊'], ['😇'], ['😍'], ['🤩'], ['😘'], ['😗'],
['😚'], ['😙'], ['😋'], ['😛'], ['😜',], ['🤪'], ['😝',], ['🤔',], ['😪'], ['😴'], ['😷'], ['🤮'], ['🥵'], ['🥶'], ['😨'], ['😰'], ['😭'], ['😱'],
['😣'], ['😞'], ['😓'], ['🥱'], ['😤'], ['😡'], ['🤬'], ['😈'], ['👿'], ['💋'], ['👋'], ['🤚'], ['🖐'], ['✋'], ['🖖'], ['👌'], ['✌'], ['🤞'], ['🤟'], ['🤙'],
['🖕'], ['👇'], ['☝'], ['👍'], ['👎'], ['👏'], ['🤲'], ['🤝'], ['🙏'],
];



$(document).ready(function () {

    for (var i = 0; i < emojisTitles.length; i++) {
        $("#hidden_emoji_box1").append('<div class="tooltip emoji_single" onclick="emojifn(this)" id="' + i + '">' + emojisTitles[i][0] + '<span class="tooltiptext">' + emojisTitles[i][1] + '</span></div>');
    }
});

function emojifn(e) {

    if (e.id == 'emoji_select_inactive') {
        $("#hidden_emoji_box").show(400);
        document.getElementById(e.id).className = 'fas fa-times';
        document.getElementById(e.id).id = 'emoji_select_active';

        $("#emoji_select_active").show();
    } else if (e.id == 'emoji_select_active') {
        $("#hidden_emoji_box").hide(400);

        document.getElementById(e.id).className = 'fas fa-laugh-beam';
        document.getElementById(e.id).id = 'emoji_select_inactive';
    }
    else if (e.className == 'tooltip emoji_single') {

        $(e).fadeOut(100);
        $(e).fadeIn(100);
        var data = document.getElementById('Query').value;
        var emojiid = e.id, temp;
        temp = emojisTitles[parseInt(emojiid)][0];
        data = data + temp;
        document.getElementById('Query').value = data;
        document.getElementById('micIcon').className = "fas fa-paper-plane";

    }
    else {
        $("#hidden_emoji_box").hide();
        document.getElementById('emoji_select_active').className = 'fas fa-laugh-beam';
        document.getElementById('emoji_select_active').id = 'emoji_select_inactive';
    }
}


$(document).ready(function () {
    wsConnect();
});

const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");


function changeIcon(iconId) {
    const inputField = document.getElementById("Query");
    const micIcon = document.getElementById(iconId);

    if (inputField.value.trim() !== "") {
        micIcon.className = "fas fa-paper-plane";
    } else {
        micIcon.className = "fas fa-microphone";
    }
}

function previewImage() {
    var file = document.getElementById("real-file").files;
    if (file.length > 0) {
        var fileReader = new FileReader();

        fileReader.onload = function (event) {
            document.getElementById("preview").setAttribute("src", event.target.result);
        };

        fileReader.readAsDataURL(file[0]);
    }
}

async function generateResponse(input) {
    const response = await fetch('/execute_chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({ question: input }),
    });

    const data = await response.json();
    return data;
}