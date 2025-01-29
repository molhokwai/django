const cardContainer = document.querySelector('.card-container');
const addCardButton = document.querySelector('.add-card');

addCardButton.addEventListener('click', () => {
    // Create the card elements
    const card = document.createElement('div');
    card.classList.add('card');

    const cardHeader = document.createElement('h3');
    cardHeader.classList.add('card-header');
    cardHeader.innerText = 'New Card';
    cardHeader.contentEditable = true;
    console.log(`cardHeader.contentEditable: ${cardHeader.contentEditable}`)

    const cardContent = document.createElement('div');
    cardContent.classList.add('card-content');
    cardContent.innerText = 'Enter content here...';
    cardContent.contentEditable = true;
    console.log(`cardContent.contentEditable: ${cardContent.contentEditable}`)
    
    const cardFooter = document.createElement('p');
    cardFooter.classList.add('card-footer');
    cardFooter.innerText = `Created: ${new Date().toLocaleDateString()}`;

    // Add elements to the card
    card.appendChild(cardHeader);
    card.appendChild(cardContent);
    card.appendChild(cardFooter);

    // Add card to the container
    cardContainer.appendChild(card);

    // Make the card draggable
    card.setAttribute('draggable', 'true');
    card.addEventListener('dragstart', (event) => {
        event.dataTransfer.setData('text/plain', card.innerText);
    });

    // Allow dropping cards anywhere on the container
    cardContainer.addEventListener('dragover', (event) => {
        event.preventDefault(); // Prevent default behavior (not allowing drops)
    });

    cardContainer.addEventListener('drop', (event) => {
        event.preventDefault(); // Prevent default behavior
        const droppedCard = event.dataTransfer.items[0].getAsElement();
        if (droppedCard !== card && droppedCard.classList.contains('card')) {
            // Check if it's a different card and prevent dropping on itself
            cardContainer.insertBefore(droppedCard, card); // Insert the dropped card before the current card
        }
    });
});
