function fetchAvatar() {
    const username = document.getElementById('username').value.trim();
    const avatarImg = document.getElementById('avatar');
    const infoMsg = document.getElementById('info');
    const errorMsg = document.getElementById('error');
    
    // Reset
    avatarImg.style.display = 'none';
    avatarImg.src = '';
    infoMsg.textContent = '';
    errorMsg.textContent = '';
    
    if (!username) {
        errorMsg.textContent = 'Please enter a username!';
        return;
    }
    
    const url = `https://www.google.com/s2/favicons?sz=256&domain_url=twitter.com/${user}`;
    
    avatarImg.onload = () => {
        avatarImg.style.display = 'block';
        infoMsg.textContent = `Profile picture for @${username}`;
    };
    
    avatarImg.onerror = () => {
        errorMsg.textContent = 'User not found or no profile picture available.';
    };
    
    avatarImg.src = url;
}
