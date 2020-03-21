$(document).ready(function () {
    var InputCount = 1;
    $("#AddMoreTextBox").click(function (e) {
        InputCount++;
        $("#InputsWrapper").append(
            '<input type="texta" name="newsa[]" ' + 'id="news_' + InputCount + '" value=""/><button>选择</button>' +
            '<input type="textb" name="newsb[]" ' + 'id="news_' + InputCount + '" value=""/><button>选择</button> <button>移除</button>' + '<br/>');
    });
});