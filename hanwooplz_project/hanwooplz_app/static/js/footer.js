let currentFrame = 1;

const gif = document.getElementById("animated-gif");

setInterval(function () {
    currentFrame = (currentFrame % 10) + 1;
    gif.src = `{% static 'img/hanwoo' %}${currentFrame}.gif`;
}, 3000);