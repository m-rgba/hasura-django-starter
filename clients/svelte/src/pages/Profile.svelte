<script>
    import { onMount } from "svelte";
    import { link } from "svelte-routing";
    import { token } from '../shared/auth.js'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    let pageRetry = 1;

    let successMessage;
    let errorMessage;

    let username = localStorage.getItem('user_name');
    let email = localStorage.getItem('user_email');
    let newEmail;

    let passwordOld;
    let password;
    let passwordConfirm;

    let checkpassLower;
    let checkpassUpper;
    let checkpassNumber;
    let checkpassSpecial;
    let checkPass;

    let updateEmailVariables = {};

    async function updateEmailHandler() {
        const accessToken = localStorage.getItem('token');
        pageRetry = pageRetry + 1;
        if (pageRetry >= 15){
            errorMessage = 'Wasn\'t able to reconnect. Please refresh and try again.';
            throw 'JWT Refresh Error';
        }

        const query = `
            mutation updateProfileEmail($username: String!, $newEmail: String!) {
                update_auth_user(where: {username: {_eq: $username}}, _set: {email: $newEmail}) {
                    returning {
                    username
                    }
                }
            }
        `;

        updateEmailVariables["username"] = username;
        updateEmailVariables["newEmail"] = newEmail;

        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
                Authorization: "Bearer " + accessToken,
            },
            body: JSON.stringify({
                query: query,
                variables: updateEmailVariables
            })
        });
        if (request.ok) {
            const response = await request.json();
            if (response.errors){
                if(response.errors[0].extensions.code === 'invalid-jwt'){ 
                    await new Promise(r => setTimeout(r, 500));
                    console.log('> Token Update / Reconnecting...');
                    token();
                    updateEmailHandler();
                } else {
                    errorMessage = response.errors[0].message;
                }
            } else {
                pageRetry = 1;
                email = newEmail;
                localStorage.setItem("user_email", newEmail);
                successMessage = 'Your profile\'s email has been updated.';
            }
        } else {
            errorMessage = 'There was a problem with your request: ' + request.statusText;
        }
    }

    async function updatePasswordHandler() {
        const accessToken = localStorage.getItem('token');
        pageRetry = pageRetry + 1;
        if (pageRetry >= 15){
            errorMessage = 'Wasn\'t able to reconnect. Please refresh and try again.';
            throw 'JWT Refresh Error';
        }
        if (password != passwordConfirm) {
            errorMessage = "Your passwords must match. Please enter a matching Password and Confirm Password combination.";
        } else if ( checkPass === false ){
            errorMessage = "Your passwords must be a strong password. It must contain at least one lowercase character, uppercase character, special character, and number.";
        } else {
            const request = await fetch("http://localhost:8000/api/user/change_password/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                    Authorization: "Bearer " + accessToken
                },
                body: JSON.stringify({ 
                    "old_password" : passwordOld,
                    "new_password" : password
                }),
            });
            if (request.ok) {
                pageRetry = 1;
                successMessage = 'Your password has been updated.';
            } else if(request.status===401) {
                await new Promise(r => setTimeout(r, 500));
                console.log('> Token Update / Reconnecting...');
                token();
                updatePasswordHandler();
            } else {
                errorMessage = 'There seems to be a problem with your request. Please ensure that your old password is correct.' + request.statusText;
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
</script>

<Header />

<div class="notification-area">
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
</div>

<content>
    <div class="container pt-xl mb-xl">
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6 mb-sm">
                <h1 class="mb-xs">Profile</h1>
                <a class="muted" use:link href="/users"><ion-icon name="arrow-back"></ion-icon> Back to Users</a>
            </div>
        </div>
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6">
                <div class="card mb-xs">
                    <div class="pad">
                        <p class="strong">Username</p>
                        <input class="w-100 mb-xs" disabled value="{username}" />
                        <p class="strong">Current Email</p>
                        <input class="w-100 mb-xs" disabled value="{email}" />

                        <form on:submit|preventDefault={updateEmailHandler}>
                            <p class="strong">Update Email</p>
                            <input type="email" class="w-100 mb-xs" bind:value={newEmail} placeholder="Email..." />
                            <button type="submit" class="w-100 mb-sm">Update Email</button>
                        </form>

                        <hr class="mb-xs" />

                        <form on:submit|preventDefault={updatePasswordHandler}>
                            <p class="strong">Current Password</p>
                            <input type="password" class="w-100 mb-xs" bind:value={passwordOld} placeholder="Old Password..." />
                            <p class="strong">New Password</p>
                            <input type="password" class="w-100 mb-xs" on:input={passwordStrengthCheck} on:change={passwordStrengthCheck} bind:value={password} placeholder="New Password..." />
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

                            <button type="submit" class="w-100 mb-xs">Update Password</button>
                        </form>

                    </div>
                </div>
            </div>
        </div>
    </div>
</content>

<Footer />