<script>
    import { authLoaded } from '../stores/auth.js'
    import { gqlResponseHandler } from '../shared/requests.js'

    import Cookies from 'js-cookie'
    import jwt_decode from "jwt-decode";

    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

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
    let passCheck;
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
            passCheck = true;
        }
    }

    async function signupHandler() {
        if (password != passwordConfirm) {
            errorMessage = "Your passwords must match. Please enter a matching Password and Confirm Password combination.";
        } else if ( passCheck !== true ){
            errorMessage = "Your passwords must be a strong password. It must contain at least one lowercase character, uppercase character, special character, and number.";
        } else {
            const variable = {};
            const query = `
                mutation userRegister($email: String = "", $password: String = "", $username: String = "") {
                    user_register(arg: {password: $password, username: $username, email: $email}) {
                        id
                        username
                        email
                        tokens
                    }
                }
            `;
            variable["username"] = username;
            variable["email"] = email;
            variable["password"] = password;
            const request = await fetch("http://localhost:8080/v1/graphql", {
                method: "POST",
                headers: { "Content-Type": "application/json", Accept: "application/json" },
                body: JSON.stringify({ query: query, variables: variable })
            });
            const signUpUser = await gqlResponseHandler(request);
            if (signUpUser.success === true){
                    localStorage.setItem("token", signUpUser.response.user_register.tokens.access);
                    const tokenDecoded = jwt_decode(signUpUser.response.user_register.tokens.access);
                    // We're only storing JWT items for ease of use > the backend will validate all items in queries
                    localStorage.setItem("token_expiry", tokenDecoded.exp);
                    localStorage.setItem("user_name", tokenDecoded.user_name);
                    localStorage.setItem("user_email", tokenDecoded.user_email);
                    localStorage.setItem("user_role", tokenDecoded["https://hasura.io/jwt/claims"]["x-hasura-default-role"]);
                    Cookies.set('refresh', signUpUser.response.user_register.tokens.refresh, { sameSite: 'strict' });
                    location.replace("/");
            } else {
                errorMessage = signUpUser.response;
            }
        }
    }

    async function loginHandler() {
        const variable = {};
        const query = `
            query userLogin($username: String = "", $password: String = "") {
                user_login(arg: {username: $username, password: $password}) {
                    access
                    refresh
                }
            }
        `;
        variable["username"] = username;
        variable["password"] = password;
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json" },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const loginUser = await gqlResponseHandler(request);
        if (loginUser.success === true){
                console.log(loginUser);
                localStorage.setItem("token", loginUser.response.user_login.access);
                const tokenDecoded = jwt_decode(loginUser.response.user_login.access);
                // We're only storing JWT items for ease of use > the backend will validate all items in queries
                localStorage.setItem("token_expiry", tokenDecoded.exp);
                localStorage.setItem("user_name", tokenDecoded.user_name);
                localStorage.setItem("user_email", tokenDecoded.user_email);
                localStorage.setItem("user_role", tokenDecoded["https://hasura.io/jwt/claims"]["x-hasura-default-role"]);
                Cookies.set('refresh', loginUser.response.user_login.refresh, { sameSite: 'strict' });
                location.replace("/");
        } else {
            errorMessage = loginUser.response;
        }
    }
    
    async function resetHandler() {
        const variable = {};
        const query = `
            mutation userPasswordReset($email: String = "") {
                user_password_reset(arg: {email: $email}) {
                    status
                }
            }
        `;
        variable["email"] = email;
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json" },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const resetUser = await gqlResponseHandler(request);
        if (resetUser.success === true){
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
                            <input class="w-100 mb-xs" on:keyup={passwordStrengthCheck} on:change={passwordStrengthCheck} bind:value={password} type="password" placeholder="Password..." />
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