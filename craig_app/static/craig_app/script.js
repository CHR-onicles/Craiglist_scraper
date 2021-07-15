let card_titles = document.querySelectorAll(".card-content p");

for (let index = 0; index < card_titles.length; index++) {
    if (String(card_titles[index].length > 20)){
        card_titles[index].innerText = card_titles[index].innerText.strip().slice(0, 17) + '...';
    }
}

//not working - cant load JS properly