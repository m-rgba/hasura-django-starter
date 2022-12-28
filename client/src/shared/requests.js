export async function gqlResponseHandler(request) {    
    if (request.ok) {
        const response = await request.json();
        if (response.errors){
            const success = false;
            const status = 'There seems to have been a problem with your request: ' + response.errors[0].message;
            return {success: success, response: status};
        } else {
            const success = true;
            return {success: success, response: response.data};
        }
    } else {
        const success = false;
        const status = 'There seems to have been a problem with your request: ' + request.status + ' ' + request.statusText;
        return {success: success, response: status};
    };
}

// export async function restResponseHandler(request) {    
//     if (request.ok) {
//         const response = await request.json();
//         const success = true;
//         return {success: success, response: response};
//     } else {
//         const success = false;
//         const status = 'There seems to have been a problem with your request: ' + request.status + ' ' + request.statusText;
//         return {success: success, response: status};
//     };
// }