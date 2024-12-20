var flag = 0;
async function detailClick(pillsId, serial) {
    if (flag) buyClick(pillsId, serial);
    try {
        flag = 1;
        document.getElementsByClassName("pt-3 pb-3 Roboto")[serial].getElementsByTagName("button")[0].click();
        await new Promise(resolve => setTimeout(resolve, 100));
        purchaseClick(pillsId, serial);
    } catch (e) {
        console.log(e);
        await new Promise(resolve => setTimeout(resolve, 100));
        detailClick(pillsId, serial);
    }
}

async function purchaseClick(pillsId, serial) {
    try {
        document.getElementById(pillsId).getElementsByTagName('button')[1].click();
        await new Promise(resolve => setTimeout(resolve, 100));
    } catch (e) {
        console.log(e);
        await new Promise(resolve => setTimeout(resolve, 100));
        detailClick(pillsId, serial);
    }
}

async function buyClick(pillsId, serial) {
    try {
        flag = 0;
        document.getElementsByClassName("row pt-2 pb-3 Roboto")[0].getElementsByTagName("button")[0].click();
        await new Promise(resolve => setTimeout(resolve, 100));
        agreeClick(pillsId, serial);
    } catch (e) {
        console.log(e);
        await new Promise(resolve => setTimeout(resolve, 100));
        detailClick(pillsId, serial);
    }
}

async function agreeClick(pillsId, serial) {
    try {
        document.getElementsByClassName("modal justify-content-center")[0].getElementsByTagName("button")[1].click();
        await new Promise(resolve => setTimeout(resolve, 100));
        bkashClick();
    } catch (e) {
        console.log(e);
        await new Promise(resolve => setTimeout(resolve, 100));
        detailClick(pillsId, serial);
    }
}

async function bkashClick() {
    try {
        document.getElementsByClassName("col-md-6 bg-white pt-4 pb-4 cus-r-bor1 cus-b-bor-m card-block")[0].click();
    } catch (e) {
        console.log(e);
        await new Promise(resolve => setTimeout(resolve, 100));
        bkashClick();
    }
}

detailClick("pills-route-794-tab", 3);