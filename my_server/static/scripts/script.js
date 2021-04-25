const abi = [ { "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "address", "name": "receiver", "type": "address" } ], "name": "airdropBot", "outputs": [], "stateMutability": "payable", "type": "function" }, { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "approved", "type": "address" }, { "indexed": true, "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "operator", "type": "address" }, { "indexed": false, "internalType": "bool", "name": "approved", "type": "bool" } ], "name": "ApprovalForAll", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "approve", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "burn", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "newPrice", "type": "uint256" } ], "name": "changePrice", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint16", "name": "firstID", "type": "uint16" }, { "internalType": "uint16", "name": "secondID", "type": "uint16" }, { "internalType": "bool[6]", "name": "choices", "type": "bool[6]" } ], "name": "combineBots", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "uint16", "name": "firstID", "type": "uint16" }, { "indexed": false, "internalType": "uint16", "name": "secondID", "type": "uint16" }, { "indexed": false, "internalType": "uint16", "name": "newID", "type": "uint16" }, { "indexed": false, "internalType": "uint256", "name": "bits", "type": "uint256" } ], "name": "CombinedBot", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "to", "type": "address" } ], "name": "createMint", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" } ], "name": "grantRole", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "to", "type": "address" } ], "name": "mint", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "mintBot", "outputs": [], "stateMutability": "payable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "uint16", "name": "id", "type": "uint16" }, { "indexed": false, "internalType": "uint256", "name": "bits", "type": "uint256" } ], "name": "NewBot", "type": "event" }, { "inputs": [], "name": "pause", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "account", "type": "address" } ], "name": "Paused", "type": "event" }, { "inputs": [ { "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" } ], "name": "renounceRole", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" } ], "name": "revokeRole", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "indexed": true, "internalType": "bytes32", "name": "previousAdminRole", "type": "bytes32" }, { "indexed": true, "internalType": "bytes32", "name": "newAdminRole", "type": "bytes32" } ], "name": "RoleAdminChanged", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "indexed": true, "internalType": "address", "name": "account", "type": "address" }, { "indexed": true, "internalType": "address", "name": "sender", "type": "address" } ], "name": "RoleGranted", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "indexed": true, "internalType": "address", "name": "account", "type": "address" }, { "indexed": true, "internalType": "address", "name": "sender", "type": "address" } ], "name": "RoleRevoked", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "from", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "safeTransferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "from", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" }, { "internalType": "bytes", "name": "_data", "type": "bytes" } ], "name": "safeTransferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "operator", "type": "address" }, { "internalType": "bool", "name": "approved", "type": "bool" } ], "name": "setApprovalForAll", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "baseURI", "type": "string" } ], "name": "setBaseURI", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "to", "type": "address" }, { "indexed": true, "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "from", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "transferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "unpause", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "address", "name": "account", "type": "address" } ], "name": "Unpaused", "type": "event" }, { "inputs": [], "name": "withdraw", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "owner", "type": "address" } ], "name": "balanceOf", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "contractURI", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "pure", "type": "function" }, { "inputs": [], "name": "DEFAULT_ADMIN_ROLE", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "getApproved", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint16", "name": "_id", "type": "uint16" } ], "name": "getBotBits", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "getPrice", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "role", "type": "bytes32" } ], "name": "getRoleAdmin", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "uint256", "name": "index", "type": "uint256" } ], "name": "getRoleMember", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "role", "type": "bytes32" } ], "name": "getRoleMemberCount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "role", "type": "bytes32" }, { "internalType": "address", "name": "account", "type": "address" } ], "name": "hasRole", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "owner", "type": "address" }, { "internalType": "address", "name": "operator", "type": "address" } ], "name": "isApprovedForAll", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "name", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "ownerOf", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "paused", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "PAUSER_ROLE", "outputs": [ { "internalType": "bytes32", "name": "", "type": "bytes32" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "bytes4", "name": "interfaceId", "type": "bytes4" } ], "name": "supportsInterface", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "symbol", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "index", "type": "uint256" } ], "name": "tokenByIndex", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "owner", "type": "address" }, { "internalType": "uint256", "name": "index", "type": "uint256" } ], "name": "tokenOfOwnerByIndex", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "tokenURI", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "totalMinted", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "totalSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" } ];
let contract;
let accounts;
let result;
let connected = false;
$("#connect-button").click(async function (e) { 
    if (window.ethereum) {
      window.web3 = new Web3(window.ethereum);
      await window.ethereum.enable();
      setUpBlockchain();
    }
    else if (window.web3) {
      window.web3 = new Web3(window.web3.currentProvider);
      setUpBlockchain();
    }
    else {
      window.alert("No MetaMask wallet detected!")
    }
});

async function setUpBlockchain() {
    //Display account
    accounts = await web3.eth.getAccounts();
    connected = accounts.length > 0;

    const lcontract = new web3.eth.Contract(abi, "0x69DD9B274ddeF3C8625147ccF57870E03fbef025");
    let totalMinted;
    try {
        totalMinted = await lcontract.methods.totalMinted().call();
        contract = lcontract;
        if(connected)$("#connect-button").text(accounts[0].slice(0,7)+"...");
        $(".mint-amount").text(totalMinted + " out of 2048")
        $('.mint-amount').width(""+(Math.trunc(totalMinted/2048)+1) + "%");
        $('.mint-amount').css('opacity', '1');
        $('.bots-left').text((2048-totalMinted) + " bots left!")
    } catch (error) {
        window.alert("Contract not connected to this network!");
    }
    
    console.log(totalMinted);
    if (typeof updateCombine !== "undefined") {
      updateCombine();
    }
    renderBotArrays();
}



window.onload = function() {
  if (window.web3) {
    window.web3 = new Web3(window.web3.currentProvider);
    console.log("window.web3")
    setUpBlockchain();
  } else {
    //Change to mainnet
    window.web3 = new Web3(new Web3.providers.HttpProvider('https://ropsten.infura.io/v3/df1bf651fb8b46a19b9574206b184064'));
    setUpBlockchain();
  }
};

$('.buy-now-button').click(function () {
  if ($(this).hasClass('buyable') && connected) {
    if (!contract) {
      window.alert("Not connected to the ETH network!")
    } else {
      const amount = parseInt($(".slide").val());
      $(this).html('<img class="loading-gear" src="/static/Images/loading-gear.gif"></img> Pending...')
      contract.methods.mintBot(amount).send({ from: accounts[0], value: 60000000000000000*amount }).then(
        function(res) {
          const botVals = res.events.NewBot;
          console.log(botVals);
          bots = [];
          if(Array.isArray(botVals)) {
            for (let i = 0; i < botVals.length; i++) {
              const e = botVals[i];
              bots.push(e.returnValues.id);
            }
            let index = 0;
            $(".next-btn").show().click(function() {
              if(index < bots.length-1) {index++} else {index = 0};
              $('.card-bot-name').text('Bitbot #' + bots[index]);
              $('.product').attr('src', 'http://localhost:8070/static/bots-images/'+bots[index]+'.PNG');
            });

          } else {
            bots.push(botVals.returnValues.id);
          }
          console.log(bots);
          $('.product').attr('src', 'http://localhost:8070/static/bots-images/'+bots[0]+'.PNG');
          $('.card-bot-name').text('Bitbot #' + bots[0]);
          $('.buy-now-button').html('Buy Now');
        }
      ).catch(function() {
        $(".buy-now-button").html('Buy Now');
      });   
    }
  } else {
    window.alert(connected ? "You cannot mint yet!" : "You need to connect your metamask wallet before buying!")
  }
})

async function renderBotArrays() {
  const arrayDiv = $('#bot-array');
  const type = $(arrayDiv).data('type');
  let dataId = $(arrayDiv).data('id');
  

  if(type == 'wallet') {
    if (dataId == '0') {
      dataId = accounts[0];
    }
    const balance = await contract.methods.balanceOf(accounts[0]).call();
    for (let i = 0; i < balance; i++) {
        const e = await contract.methods.tokenOfOwnerByIndex(accounts[0], i).call();
        $(arrayDiv).append(`
        <div class="card">
          <div class="card__inner" data-bot-id="${e}">
              <div class="card__face card__face--front">
                  <img src="/static/bots-images/${e}.png" alt="">
                  <h2 class="card-bot-name">Bot #${e}</h2>
                  <h2 class="card-bot-level">Level 2</h2>
              </div>
              <div class="card__face card__face--back">
                  <div class="back-card-bot-parts">
                  </div>
              </div>
          </div>
      </div>
        `);
    }
    $('.card').mouseenter(function() {
      const inner = $(this).children('.card__inner');
      const id = $(inner).data("bot-id");
      if(!$(inner).addClass('is-flipped').hasClass('generated')) {
        $(inner).addClass('generated');
        $.ajax({
          type: "GET",
          url: "/_bot_serial/"+id,
          dataType: "JSON",
          success: function (r) {
            console.log(r);
            $(inner).find('.back-card-bot-parts').append(`
            <div class="head">
              <h2>Head</h2>
              <p><span>PART OF: </span>${r.head.name}<br>
                  <span>RARITY:</span> ${r.head.category.rarity}, only ${r.head.amount} in existence</p>
              <hr/>
          </div>
          <div class="body">
              <h2>Body</h2>
              <p><span>PART OF: </span>${r.body.name}<br>
                  <span>RARITY:</span> ${r.body.category.rarity}, only ${r.body.amount} in existence</p>
              <hr/>
          </div>
          <div class="right-arm">
              <h2>Right Arm</h2>
              <p><span>PART OF: </span>${r.right_arm.name}<br>
                  <span>RARITY:</span> ${r.right_arm.category.rarity}, only ${r.right_arm.amount} in existence</p>
              <hr/>
          </div>
          <div class="left-arm">
              <h2>Left Arm</h2>
              <p><span>PART OF: </span>${r.left_arm.name}<br>
                  <span>RARITY:</span> ${r.left_arm.category.rarity}, only ${r.left_arm.amount} in existence</p>
              <hr/>
          </div>
          <div class="right-leg">
              <h2>Right Leg</h2>
              <p><span>PART OF: </span>${r.right_leg.name}<br>
                  <span>RARITY:</span> ${r.right_leg.category.rarity}, only ${r.right_leg.amount} in existence</p>
              <hr/>
          </div>
          <div class="left-leg">
              <h2>Left Leg</h2>
              <p><span>PART OF: </span>${r.left_leg.name}<br>
                  <span>RARITY:</span> ${r.left_leg.category.rarity}, only ${r.left_leg.amount} in existence</p>
          </div>
            `);
          }
        });
      };
    }).mouseleave(function() {
      $(this).children('.card__inner').removeClass('is-flipped');
    })
  }
}

$(".branch").each(function() {
  const children = $(this).children('.branch-children').children('img')
  const secChildren = $(this).children('.branch-children').children(".branch").children('img')
  const from = $(this).children('img')
  $().connections({ from: from,  to: $(children)})
  $().connections({ from: from,  to: $(secChildren)})
})
  
$('.card').mouseenter(function() {
  const inner = $(this).children('.card__inner');
  const id = $(inner).data("bot-id");
  if(!$(inner).addClass('is-flipped').hasClass('generated')) {
    $(inner).addClass('generated');
    $.ajax({
      type: "GET",
      url: "/_bot_serial/"+id,
      dataType: "JSON",
      success: function (r) {
        console.log(r);
        $(inner).find('.back-card-bot-parts').append(`
        <div class="head">
          <h2>Head</h2>
          <p><span>PART OF: </span>${r.head.name}<br>
              <span>RARITY:</span> ${r.head.category.rarity}, only ${r.head.amount} in existence</p>
          <hr/>
      </div>
      <div class="body">
          <h2>Body</h2>
          <p><span>PART OF: </span>${r.body.name}<br>
              <span>RARITY:</span> ${r.body.category.rarity}, only ${r.body.amount} in existence</p>
          <hr/>
      </div>
      <div class="right-arm">
          <h2>Right Arm</h2>
          <p><span>PART OF: </span>${r.right_arm.name}<br>
              <span>RARITY:</span> ${r.right_arm.category.rarity}, only ${r.right_arm.amount} in existence</p>
          <hr/>
      </div>
      <div class="left-arm">
          <h2>Left Arm</h2>
          <p><span>PART OF: </span>${r.left_arm.name}<br>
              <span>RARITY:</span> ${r.left_arm.category.rarity}, only ${r.left_arm.amount} in existence</p>
          <hr/>
      </div>
      <div class="right-leg">
          <h2>Right Leg</h2>
          <p><span>PART OF: </span>${r.right_leg.name}<br>
              <span>RARITY:</span> ${r.right_leg.category.rarity}, only ${r.right_leg.amount} in existence</p>
          <hr/>
      </div>
      <div class="left-leg">
          <h2>Left Leg</h2>
          <p><span>PART OF: </span>${r.left_leg.name}<br>
              <span>RARITY:</span> ${r.left_leg.category.rarity}, only ${r.left_leg.amount} in existence</p>
      </div>
        `);
      }
    });
  };
}).mouseleave(function() {
  $(this).children('.card__inner').removeClass('is-flipped');
})

var countDownDate = new Date(Date.UTC(2021, 3, 25, 10, 45, 0)).getTime();

var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  document.getElementById("demo").innerHTML = hours + "h "
  + minutes + "m " + seconds + "s ";

  //If the count down is finished, write some text
  if (distance < 0) {
    clearInterval(x);
    $('#demo').html("");
    $('.buy-now-button').addClass('buyable');
  }
}, 1000);