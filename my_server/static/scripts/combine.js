let parts = [null, null, null, null, null, null];
let bot1;
let bot2;

async function updateCombine() {
    const balance = await contract.methods.balanceOf(accounts[0]).call();
    for (let i = 0; i < balance; i++) {
        const e = await contract.methods.tokenOfOwnerByIndex(accounts[0], i).call();
        $(".dropdown-content")
        .append(`<div class="drop-element" data-bot-id="${e}"><img src="static/bots-images/${e}.png")}}"><h2>Bot #${e}</h2></div>`);
    }

    $("#forge-button").click(function (e) { 
        if (parts[0] != undefined && parts[1] != undefined && parts[2] != undefined && parts[3] != undefined && parts[4] != undefined && parts[5] != undefined) {
            $('.forge-animation').children('img').attr('src', '/static/Images/door-animation.gif')
            $('.hidden').removeClass('hidden');
            $("#forge-button").html('<img class="loading-gear" src="/static/Images/loading-gear.gif"></img> Pending...');
            contract.methods.combineBots(bot1.id, bot2.id, parts).send({ from: accounts[0]}).then(
                function(res) {
                    const bot = res.events.NewBot.returnValues;
                    console.log(bot)
                    $('.result').html(`
                        <h3 id="lvl-pre">Bot #${bot.id}</h3>
                        <img class="product" src="static/bots-images/${bot.id}.png">
                        <div class="forge-animation">
                            <img src="" alt="">
                        </div>
                    `);
                    $('.forge-animation').children('img').attr('src', '/static/Images/door-animation-open.gif')
                    $("#forge-button").html('FORGE NOW');
                }
            ).on('error', function() {
                console.log('error something')
                $('.forge-animation').children('img').attr('src', '/static/Images/door-animation-open.gif')
                $("#forge-button").html('FORGE NOW');
            });  
        } else {
            window.alert("All 6 parts need to be selected to forge!")
        }
    });

    $('.drop-element').click(function() {
        const value = $(this).data('bot-id');
        const pick = $(this).parent().hasClass('pick-1') ? "1" : "2";
        $.ajax({
            type: "GET",
            url: "/_bot_serial/" + value,
            dataType: "JSON",
            success: function (r) {
                if(pick == "1"){bot1 = r} else {bot2 = r}
                $('#pre-head'+pick).attr("src", "static/"+r.head.image);
                $('#pre-body'+pick).attr("src", "static/"+r.body.image);
                $('#pre-l_arm'+pick).attr("src", "static/"+r.left_arm.image);
                $('#pre-r_arm'+pick).attr("src", "static/"+r.right_arm.image);
                $('#pre-l_leg'+pick).attr("src", "static/"+r.left_leg.image);
                $('#pre-r_leg'+pick).attr("src", "static/"+r.right_leg.image);
                $('#lvl-pre-'+pick).text("Level " + r.level);
                updatePreview();
            }
        }); 
    });
}

$(".part").click(function() {
    const isFirst = $(this).parent().hasClass("first");
    console.log(bot1 + " " + bot2)
    if ((isFirst ? bot1 : bot2) == undefined) {
        return
    }
    const part = $(this).attr("class").split(/\s+/)[1];
    $("."+part).parent().removeClass("selected").addClass("not-selected");
    $(this).parent().addClass("selected").removeClass("not-selected");
    parts[parseInt(part)] = !isFirst;
    updatePreview();
});

function updatePreview() {
    if(parts[0] !== null) $('#pre-head').attr("src", "static/"+  (parts[0] ? bot2 : bot1).head.image);
    if(parts[1] !== null) $('#pre-body').attr("src", "static/"+  (parts[1] ? bot2 : bot1).body.image);
    if(parts[2] !== null) $('#pre-l_arm').attr("src", "static/"+ (parts[2] ? bot2 : bot1).left_arm.image);
    if(parts[3] !== null) $('#pre-r_arm').attr("src", "static/"+ (parts[3] ? bot2 : bot1).right_arm.image);
    if(parts[4] !== null) $('#pre-l_leg').attr("src", "static/"+ (parts[4] ? bot2 : bot1).left_leg.image);
    if(parts[5] !== null) $('#pre-r_leg').attr("src", "static/"+ (parts[5] ? bot2 : bot1).right_leg.image);
    if(bot1 != undefined && bot2 != undefined) $('#lvl-pre').text("Level " + (bot1.level == bot2.level ? bot1.level+1 : bot1.level > bot2.level ? bot1.level : bot2.level));
}