const logGameData = () => {
    const correctOnepicked = selectedImages.filter(item => item.choice === "high");
    const wrongOnepicked = selectedImages.filter(item => item.choice === "low");
    const score = correctOnepicked.length;
    const timestamp = new Date().toISOString();
  
    const gameResult = {
      userId,
      userEmail,
      score,
      correct_one_picked: correctOnepicked,
      wrong_one_picked: wrongOnepicked,
      gamedomain: from,
      timestamp,
    };
  
    fetch('/api/store-game/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(gameResult),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };