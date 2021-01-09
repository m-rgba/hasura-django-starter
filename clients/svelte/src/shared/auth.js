import { authLoaded } from '../stores/auth.js'
import Cookies from 'js-cookie'
import jwt_decode from "jwt-decode";

export async function token(redirect) {
    // console.log('> Running token();')
    const refresh = Cookies.get('refresh');
    const accessToken = localStorage.getItem('token');
    const accessExpiry = localStorage.getItem("token_expiry");
    const currentTime = Date.now();
    const currentTimeTrim = (currentTime-(currentTime%1000))/1000;
    if (accessToken && currentTimeTrim >= accessExpiry || !accessToken && refresh) {
        // console.log('> No Access Token / Expired > Getting New Token');
        const request = await fetch("http://localhost:8000/api/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({ 
                "refresh" : refresh 
            }),
        });
        if (request.ok) {
            // console.log('> Parsing new token')
            const response = await request.json();
            const tokenResponse = response.access;
            const tokenDecoded = jwt_decode(tokenResponse);
            // Load up new token > go home / we'll stash role and user name for display reasons (permissions are handled Hasura/Django-side)
            // Stashing expiry for token expiry to know when to re-run the token refresh
            localStorage.setItem("token", tokenResponse);
            localStorage.setItem("token_expiry", tokenDecoded.exp);
            localStorage.setItem("user_name", tokenDecoded.user_name);
            localStorage.setItem("user_email", tokenDecoded.user_email);
            localStorage.setItem("user_id", tokenDecoded["https://hasura.io/jwt/claims"]["x-hasura-user-id"]);
            localStorage.setItem("user_role", tokenDecoded["https://hasura.io/jwt/claims"]["x-hasura-default-role"]);
            authLoaded.set(true);
            return(tokenResponse);
        } else {
            // console.log('> Getting new token failed > Clearing tokens')
            clearTokens(redirect);
        }
    } else if (!refresh){
        // console.log('> No refresh token > Clearing tokens')
        clearTokens(redirect);
    } else {
        // All good, return old access token
        authLoaded.set(true);
        return(accessToken);
    }
};

function clearTokens(redirect) {
    // Clear everything > go to login
    localStorage.setItem("token", "");
    Cookies.set('refresh', "", { sameSite: 'strict' })
    localStorage.setItem("token_expiry", "");
    localStorage.setItem("user_name", "");
    localStorage.setItem("user_email", "");
    localStorage.setItem("user_role", "");
    authLoaded.set(true);
    if (redirect != false){
        location.replace("/");
    };
};