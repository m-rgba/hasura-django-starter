<script>
    import { onMount } from "svelte";
    import { navigate, link } from "svelte-routing";
    import { gqlResponseHandler } from '../shared/requests.js'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

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
                headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
                body: JSON.stringify({ query: query, variables: variable })
            });
            const createUser = await gqlResponseHandler(request);
            if (createUser.success === true){
                navigate("/users?created=true", { replace: true });
            } else {
                errorMessage = createUser.response;
            }  
        }
    }
</script>

<Header />

<content>
    <div class="container pt-xl mb-xl">
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6 mb-sm">
                <h1 class="mb-xs">Create User</h1>
                <a class="muted" use:link href="/users"><ion-icon name="arrow-back"></ion-icon> Back to Users</a>
            </div>
        </div>
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6">
                <div class="card mb-xs">
                    <div class="pad">
                        {#if errorMessage}
                            <div class="notification mb-xs negative">
                                <a on:click={() => errorMessage = ''} style="color:#fff; float:right;" href="#!"><ion-icon name="close"></ion-icon></a>
                                <p>{errorMessage}</p>
                            </div>            
                        {/if}

                        <form on:submit|preventDefault={signupHandler}>
                            <p class="strong">Username</p>
                            <input class="w-100 mb-xs" bind:value={username} placeholder="Username..." />
                            <p class="strong">Email</p>
                            <input class="w-100 mb-xs" bind:value={email} placeholder="Email..." />
                            <p class="strong">Password</p>
                            <input type="password" class="w-100 mb-xs" on:keyup={passwordStrengthCheck} on:change={passwordStrengthCheck} bind:value={password} placeholder="Password..." />
                            <p class="strong">Confirm Password</p>
                            <input type="password" class="w-100 mb-xs" bind:value={passwordConfirm} placeholder="Confirm Password..." />

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

                            <button type="submit" class="w-100 mb-xs">Create User</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</content>

<Footer />