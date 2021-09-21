"use strict";

const $cupcakeList = $(".cupcake-list");
const $form = $(".cupcake-form");

/** A function that uses Axios to get a list of all cupcakes*/

async function getCupcakeList() {
    let response = await axios.get('/api/cupcakes');
    let cupcakes = response.data.cupcakes;

    return cupcakes;
}

/** Takes list of all cupcakes and generates HTML and displays on page 
*/
function showCupcakeList(cupcakes) {

    for (let cupcake of cupcakes) {
        createHTMLForCupcake(cupcake);
    }
}


/** Creates the HTML markup for a single cupcake */

function createHTMLForCupcake(cupcake) {
    let $divCupcake = $("<div>").addClass("col-4");
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

/** Sends new cupcake data to the API as { flavor, size, rating, image }
 * and returns form data about the new cupcake
 */

async function createNewCupcakeToAPI() {
    console.log("createNewCupcakeToAPI Beginning happening");
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const image = $("#image").val();
    const response = await axios({
        url: "/api/cupcakes",
        method: "POST",
        data: { flavor, size, rating, image },
    });

    const cupcake = response.data.cupcake;
    createHTMLForCupcake(cupcake);

    return cupcake;
}

/** Process form submit to add new cupcake to the database */
async function handleNewCupcakeFormSubmit(evt) {
    evt.preventDefault();

    await createNewCupcakeToAPI();
}

$form.on("submit", handleNewCupcakeFormSubmit);

/**  Creates cupcake list on page load */

async function start() {
    let cupcakes = await getCupcakeList();
    showCupcakeList(cupcakes);
}

start();