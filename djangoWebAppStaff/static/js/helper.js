/*
    Helper functions for frontend js code.
*/

export const getFullUrl = (endpoint) => {
    /* Obtain full url path for the given endpoint dynamically. */
    const baseUrl = window.location.href.split('/').slice(0, 3).join('/');
    return `${baseUrl}${endpoint}`;
};