"use strict";

const $cupcakeList = $(".cupcake-list");
const $form = $(".cupcake-form");

/** A function that uses Axios to get a list of all cupcakes
 *  and then adds each cupcake to the homepage
 */
async function getList() {
    let response = await axios.get('/api/cupcakes');
    let cupcakes = response.data.cupcakes;

    for (let cupcake of cupcakes) {
        createHTMLForCupcake(cupcake);        
    }

}

function createHTMLForCupcake(cupcake) {
    let $divCupcake = $("<div col-4>");
        let $cupcakeFlavor = $("<h2>").text(`Flavor: ${cupcake.flavor}`);
        let $cupcakeSize = $("<li>").text(`Size: ${cupcake.size}`);
        let $cupcakeRating = $("<li>").text(`Rating: ${cupcake.rating}`);
        let $cupcakeImage = $("<img>").attr("src", `${cupcake.image}`).addClass("img-fluid")
        $divCupcake
            .append($cupcakeFlavor)
            .append($cupcakeSize)
            .append($cupcakeRating)
            .append($cupcakeImage);
        $cupcakeList.append($divCupcake);            
}

async function createNewCupcakeToAPI() {
    console.log("createNewCupcakeToAPI Beginning happening");
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const image = $("#image").val();
    const response = await axios ({
        url: "/api/cupcakes",
        method: "POST",
        data: {flavor, size, rating, image},
    });

    cupcake = response.data.cupcake;
    createHTMLForCupcake(cupcake);

    return response.data.cupcake;
}

async function handleNewCupcakeFormSubmit(evt) {
    evt.preventDefault();
    console.log("handleNewCupcakeFormSubmit is happening");
    debugger;

    response = await createNewCupcakeToAPI();
    return response;
}

// add event listener
$form.on("submit", handleNewCupcakeFormSubmit);

async function start() {
    await getList();
}

start();