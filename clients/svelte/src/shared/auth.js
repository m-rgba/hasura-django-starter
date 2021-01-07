import { authLoaded } from '../stores/auth.js'

import Cookies from 'js-cookie'
import jwt_decode from "jwt-decode";

export function token(redirect) {
    const refresh = Cookies.get('refresh');
    const accessToken = localStorage.getItem('token');

    // console.log('> token(); Triggered');
    if (!accessToken){
        if (refresh){
            // console.log('> Refreshing Token');
            tokenRefresh(redirect);
        } else {
            // console.log('> Handling No Token');
            noToken(redirect);
        }
    } else {
        const accessExpiry = localStorage.getItem("token_expiry");
        const currentTime = Date.now();
        const currentTimeTrim = (currentTime-(currentTime%1000))/1000;
        if (currentTimeTrim >= accessExpiry) {
            // console.log('> Expired > Getting New Token')
            tokenRefresh();
        };
        authLoaded.set(true);
    }
}

function noToken(redirect) {
    // console.log('> No Token Found');
    authLoaded.set(true);
    if (redirect != false){
        location.replace("/login");
    }
}

async function tokenRefresh(redirect) {
    const refresh = Cookies.get('refresh');
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
        const response = await request.json();
        if (response.access){
            const tokenResponse = response.access
            const tokenDecoded = jwt_decode(tokenResponse);
            // Load up new token > go home / we'll stash role and user name for display reasons (permissions are handled Hasura/Django-side)
            // Stashing expiry for token expiry to know when to re-run the token refresh
            localStorage.setItem("token", tokenResponse);
            localStorage.setItem("token_expiry", tokenDecoded.exp);
            localStorage.setItem("user_name", tokenDecoded.user_name);
            localStorage.setItem("user_email", tokenDecoded.user_email);
            localStorage.setItem("user_role", tokenDecoded["https://hasura.io/jwt/claims"]["x-hasura-default-role"]);
            authLoaded.set(true);
        } else {
            // Clear everything > go to login
            localStorage.setItem("token", "");
            Cookies.set('refresh', "", { sameSite: 'strict' })
            authLoaded.set(true);
        }
    } else {
        localStorage.setItem("token", "");
        Cookies.set('refresh', "", { sameSite: 'strict' })
        authLoaded.set(true);
        if (redirect != false){
            location.replace("/login");
        };
    }
}