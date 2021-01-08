export async function gqlResponseHandler(request) {    
    if (request.ok) {
        // console.log('> Request Success');
        const response = await request.json();
        if (response.errors){
            const success = false;
            const status = 'There seems to have been a problem with your request: ' + response.errors[0].message;
            if(response.errors[0].extensions.code === 'invalid-jwt'){ 
                token();
                // console.log('> Query Errors > Token');
                return {success: success, response: status};
            } else {
                // console.log('> Query Errors > General');
                return {success: success, response: status};
            }
        } else {
            // console.log('> Query Success');
            const success = true;
            return {success: success, response: response.data};
        }
    } else {
        // console.log('> Request Failed');
        const success = false;
        const status = 'There seems to have been a problem with your request: ' + request.status + ' ' + request.statusText;
        return {success: success, response: status};
    };
}

export async function restResponseHandler(request) {    
    if (request.ok) {
        const response = await request.json();
        // console.log('> Request Success');
        const success = true;
        return {success: success, response: response};
    } else {
        // console.log('> Request Failed');
        const success = false;
        const status = 'There seems to have been a problem with your request: ' + request.status + ' ' + request.statusText;
        return {success: success, response: status};
    };
}