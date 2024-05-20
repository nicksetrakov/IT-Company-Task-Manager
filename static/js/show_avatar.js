document.addEventListener('DOMContentLoaded', (event) => {
    let avatarInput = document.getElementById('id_avatar');
    let avatarPreview = document.createElement('img');
    avatarPreview.style.width = '40px';
    avatarPreview.style.height = '40px';
    avatarPreview.style.display = 'none';
    avatarPreview.style.marginBottom = '10px';

    avatarInput.parentNode.insertBefore(avatarPreview, avatarInput);

    function updateAvatarPreview() {
        let url = avatarInput.value;

        if (url) {
            avatarPreview.src = url;
            avatarPreview.style.display = 'block';
        } else {
            avatarPreview.style.display = 'none';
        }
    }

    updateAvatarPreview();
    avatarInput.addEventListener('input', updateAvatarPreview);
});