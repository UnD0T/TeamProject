// document.querySelectorAll('.img-container img').forEach(img =>{
//     img.onclick = () => {
//         document.querySelector('.pop-up').style.display = 'block'
//         document.querySelector('.pop-up img').src = img.getAttribute('src') 
//     }
// });

// document.querySelector('.pop-up span').onclick = () => {
//         document.querySelector('.pop-up').style.display = 'none'
//     }


document.getElementsByClassName(".product-image").onclick = () => {
    document.getElementsByClassName('.pop-up').style.display = 'block'
    document.getElementsByClassName('.product-image').src = document.querySelector("product-image").getAttribute('src')
}


// document.querySelector('.pop-up-span').onclick = () => {
//     document.querySelector('.pop-up').style.display = 'none'
// }



document.getElementsByClassName('.pop-up-span').addEventListener("click", function() {
    // document.querySelector("pop-up").style.display = 'none';
    // document.querySelector("span").style.display = "none";
    document.getElementById("pop-up").style.display = "none"
})