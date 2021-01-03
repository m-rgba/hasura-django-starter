<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import Cookies from 'js-cookie'
    import { authToken } from '../stores/auth.js'

    // let urlParams = new URLSearchParams(window.location.search);

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    // Vars
    let authType = "Login";
    let successMessage;
    let errorMessage;

    let username;
    let email;
    let password;
    let passwordConfirm;

    let checkpassLower;
    let checkpassUpper;
    let checkpassNumber;
    let checkpassSpecial;
    let checkPass;

    onMount(() => {
        console.log($authToken)
        console.log(Cookies.get('refresh'));
    });

    async function signupHandler() {
        if (password != passwordConfirm) {
            errorMessage = "Your passwords must match. Please enter a matching Password and Confirm Password combination.";
        } else if ( checkPass === false ){
            errorMessage = "Your passwords must be a strong password. It must contain at least one lowercase character, uppercase character, special character, and number.";
        } else {
            const request = await fetch("http://localhost:8000/api/user/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                body: JSON.stringify({ username, email, password }),
            });
            if (request.ok) {
                const response = await request.json();
                if (response.tokens.access){
                    $authToken = response.tokens.access;
                    Cookies.set('refresh', response.tokens.refresh);
                    navigate("/", { replace: true });
                } else {
                    errorMessage = 'There was a problem with your request: Internal key error. Please try again.'
                }
            } else {
                try{
                    const response = await request.json();
                    errorMessage = response.username[0];
                } catch {
                    errorMessage = 'There was a problem with your request: ' + request.statusText;
                }
            }
        }
    }

    function passwordStrengthCheck() {
        if (password.match(/[a-z]+/)){
            checkpassLower = true;
        } else {
            checkpassLower = false;
        }
        if (password.match(/[A-Z]+/)){
            checkpassUpper = true;
        } else {
            checkpassUpper = false;
        }
        if (password.match(/[0-9]+/)){
            checkpassNumber = true;
        } else {
            checkpassNumber = false;
        }
        if (password.match(/[$@#&!-]+/)){
            checkpassSpecial = true;
        } else {
            checkpassSpecial = false;
        }
        if ((checkpassLower === true) && (checkpassUpper === true) && (checkpassNumber === true) && (checkpassSpecial === true)){
            checkPass = true; 
        } else {
            checkPass = false; 
        }
    }

    async function loginHandler() {
        const request = await fetch("http://localhost:8000/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({ username, password }),
        });
        if (request.ok) {
            const response = await request.json();
            if (response.access){
                $authToken = response.access;
                Cookies.set('refresh', response.refresh);
                navigate("/", { replace: true });
            } else {
                errorMessage = 'There was a problem with your request: Internal key error. Please try again.'
            }
        } else {
            errorMessage = 'There was a problem with your request: ' + request.statusText;
        }
    }

    async function resetHandler() {
        const request = await fetch("http://localhost:8000/api/user/reset_password/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({ email }),
        });
        if (request.ok) {
            successMessage = 'We\'ve sent you an email to confirm your account. Selecting the link from your email will allow you to reset the password to your account.';
        } else {
            errorMessage = 'It looks like there was a problem. This could be because that email isn\'t associated with any accounts in our system. Please try again.';
        }
    }
</script>

<Header headerType="auth" />

<content>
    <div class="container pt-xl mb-xl">
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6 mb-sm">
                <h1>{authType}</h1>
            </div>
        </div>
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6">
                <div class="card mb-xs">
                    <div class="pad">

                    {#if successMessage}
                        <div class="notification mb-xs positive">
                            <a on:click={() => successMessage = ''} style="color:#fff; float:right;" href="#!"><ion-icon name="close"></ion-icon></a>
                            <p>{successMessage}</p>
                        </div>            
                    {/if}
                    {#if errorMessage}
                        <div class="notification mb-xs negative">
                            <a on:click={() => errorMessage = ''} style="color:#fff; float:right;" href="#!"><ion-icon name="close"></ion-icon></a>
                            <p>{errorMessage}</p>
                        </div>            
                    {/if}

                    {#if authType === "Login"}
                        <form on:submit|preventDefault={loginHandler}>
                            <p class="strong">Username</p>
                            <input class="w-100 mb-xs" bind:value={username} placeholder="Username..." />
                            <p class="strong">Password</p>
                            <input class="w-100 mb-xs" bind:value={password} type="password" placeholder="Password..." />
                            <button type="submit" class="primary w-100 mb-xs">Login</button>    
                        </form>
                        <a on:click={() => authType = 'Reset Password'} href="#!"><p class="strong w-100 center mb-sm">Help Me Reset My Password</p></a>
                        <hr class="mb-sm" />
                        <button on:click={() => authType = 'Sign Up'} class="w-100 mb-xs">Create a New Account Instead</button>
                    {:else if authType === "Sign Up"}
                        <form on:submit|preventDefault={signupHandler}>
                            <p class="strong">Username</p>
                            <input class="w-100 mb-xs" bind:value={username} placeholder="Username..." />
                            <p class="strong">Email</p>
                            <input class="w-100 mb-xs" bind:value={email} type="email" placeholder="Email..." />
                            <p class="strong">Password</p>
                            <input class="w-100 mb-xs" on:input={passwordStrengthCheck} on:change={passwordStrengthCheck} bind:value={password} type="password" placeholder="Password..." />
                            <p class="strong">Confirm Password</p>
                            <input class="w-100 mb-xs" bind:value={passwordConfirm} type="password" placeholder="Password..." />

                            <div class="mb-xs">
                                <p> Your password must contain at least:</p>
                                <p>
                                    {#if checkpassLower === true}
                                        <ion-icon class="green" name="checkmark"></ion-icon>
                                    {:else}
                                        <ion-icon class="red" name="close"></ion-icon>
                                    {/if}
                                    1 Lowercase Character (a-z)
                                </p>
                                <p>
                                    {#if checkpassUpper === true}
                                        <ion-icon class="green" name="checkmark"></ion-icon>
                                    {:else}
                                        <ion-icon class="red" name="close"></ion-icon>
                                    {/if}
                                    1 Uppercase Character (A-Z)
                                </p>
                                <p>
                                    {#if checkpassNumber === true}
                                        <ion-icon class="green" name="checkmark"></ion-icon>
                                    {:else}
                                        <ion-icon class="red" name="close"></ion-icon>
                                    {/if}
                                    1 Number (0-9)
                                </p>
                                <p>
                                    {#if checkpassSpecial === true}
                                        <ion-icon class="green" name="checkmark"></ion-icon>
                                    {:else}
                                        <ion-icon class="red" name="close"></ion-icon>
                                    {/if}
                                    1 Special Character ($@#&!-)
                                </p>
                            </div>

                            <button type="submit" class="primary w-100 mb-xs">Create Account</button>                              
                        </form>
                        <a on:click={() => authType = 'Reset Password'} href="#!"><p class="strong w-100 center mb-sm">Help Me Reset My Password</p></a>
                        <hr class="mb-sm" />
                        <button on:click={() => authType = 'Login'} class="w-100 mb-xs">Login With My Account Instead</button>
                    {:else if authType === "Reset Password"}
                        <form on:submit|preventDefault={resetHandler}>
                            <p class="strong">Email</p>
                            <input class="w-100 mb-xs" type="email" bind:value={email} placeholder="Email..." />
                            <button type="submit" class="primary w-100 mb-sm">Request Password Reset</button>    
                        </form>
                        <hr class="mb-sm" />
                        <button on:click={() => authType = 'Login'} class="w-100 mb-xs">Login With My Account</button>
                        <button on:click={() => authType = 'Sign Up'} class="w-100 mb-xs">Create a New Account</button>
                    {/if}

                    </div>
                </div>
            </div>
        </div>
    </div>
</content>

<Footer />