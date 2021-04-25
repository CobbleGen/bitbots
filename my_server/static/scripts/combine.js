// var botSelect1 = new BVSelect({
//     selector: "#selectbotbox1",
//     searchbox: true
// });

// var botSelect2 = new BVSelect({
//     selector: "#selectbotbox2",
//     searchbox: true
// });
let parts = [null, null, null, null, null, null];
let bot1;
let bot2;

async function updateCombine() {
    const balance = await contract.methods.balanceOf(accounts[0]).call();
    //let options = {};
    for (let i = 0; i < balance; i++) {
        const e = await contract.methods.tokenOfOwnerByIndex(accounts[0], i).call();
        // options[i] = {
        //     inner_text: 'BitBot ' + e,
        //     value:      e,
        //     img:        "http://localhost:8070/static/bots-images/"+e+".png"
        // };
        $("#selectbotbox1").append('<option value="'+e+'">Bitbot #'+e+'</option>');
        $("#selectbotbox2").append('<option value="'+e+'">Bitbot #'+e+'</option>');
    }
    // botSelect1.AppendOption({
    //     position: "afterbegin",
    //     options: options
    // });
    // botSelect2.AppendOption({
    //     position: "afterbegin",
    //     options: options
    // });
    // botSelect1.Update();
    // botSelect2.Update();

    $("#combine-btn").click(function (e) { 
        let bot1 = parseInt($("#selectbotbox1").val());
        let bot2 = parseInt($("#selectbotbox2").val());

        contract.methods.combineBots(bot1, bot2, parts).send({ from: accounts[0]}).then(
            function(res) {
                const bot = res.events.NewBot.returnValues;
              }
          );  
    });
}

$("#selectbotbox1").change(function() {
    const value = $(this).val();
    $('#select-img1').attr('src','/static/bots-images/'+value+'.png');
    $.ajax({
        type: "GET",
        url: "/_bot_serial/" + value,
        dataType: "JSON",
        success: function (r) {
            bot1 = r;
            $('#head1').attr("src", "static/"+r.head.image);
            $('#body1').attr("src", "static/"+r.body.image);
            $('#l_arm1').attr("src", "static/"+r.left_arm.image);
            $('#r_arm1').attr("src", "static/"+r.right_arm.image);
            $('#l_leg1').attr("src", "static/"+r.left_leg.image);
            $('#r_leg1').attr("src", "static/"+r.right_leg.image);
            $('#lvl-1').text("Level " + r.level);
            updatePreview();
        }
    });
})

$("#selectbotbox2").change(function() {
    const value = $(this).val();
    $('#select-img2').attr('src','/static/bots-images/'+value+'.png');    
    $.ajax({
        type: "GET",
        url: "/_bot_serial/" + value,
        dataType: "JSON",
        success: function (r) {
            bot2 = r;
            $('#head2').attr("src", "static/"+r.head.image);
            $('#body2').attr("src", "static/"+r.body.image);
            $('#l_arm2').attr("src", "static/"+r.left_arm.image);
            $('#r_arm2').attr("src", "static/"+r.right_arm.image);
            $('#l_leg2').attr("src", "static/"+r.left_leg.image);
            $('#r_leg2').attr("src", "static/"+r.right_leg.image);
            $('#lvl-2').text("Level " + r.level);
            updatePreview();
        }
    });
})

$(".part").click(function() {
    const isFirst = $(this).parent().is("#first");
    if ((isFirst ? bot1 : bot2) == undefined) {
        return
    }
    const part = $(this).attr("class").split(/\s+/)[2];
    $("."+part).removeClass("selected").addClass("not-selected");
    $(this).addClass("selected").removeClass("not-selected");
    parts[$(this).index()] = !isFirst;
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

const popup = document.querySelector('.forge-animation');

function togglePopup(){
    popup.classList.toggle('hidden');
}