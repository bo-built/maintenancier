function getCookie(name) {
    // Fetch and return a cookie from the document of given name
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getNextParam() {
    // Search the URL for a "next" query param
    // If it exusts and if it is safely formatted, return it
    const urlParams = new URLSearchParams(window.location.search);
    const nextUrl = urlParams.get('next');

    const isSafeNext = nextUrl && nextUrl.startsWith('/') && !nextUrl.startsWith('//');

    if(isSafeNext) {
        return nextUrl;
    }
    return false;
}

function showLoadedData() {
    /*
        Relies on an element with ID "loading-placeholder"
        and one with ID ""
    */
   document.getElementById('loading-placeholder').classList.add('hidden');
   document.getElementById('loaded-data').classList.remove('hidden');
}