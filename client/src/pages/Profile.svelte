<script>
    import { onMount } from "svelte";
    import { link } from "svelte-routing";
    import { token } from '../shared/auth.js'
    import { gqlResponseHandler } from '../shared/requests.js'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

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

    async function updateEmailHandler() {
        const variable = {};
        const query = `
            mutation updateProfileEmail($username: String!, $newEmail: String!) {
                update_auth_user(where: {username: {_eq: $username}}, _set: {email: $newEmail}) {
                    returning {
                    username
                    }
                }
            }
        `;
        variable["username"] = username;
        variable["newEmail"] = newEmail;
        const accessToken = await token();
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const updateEmail = await gqlResponseHandler(request);
        if (updateEmail.success === true){
            email = newEmail;
            localStorage.setItem("user_email", newEmail);
            successMessage = 'Your profile\'s email has been updated.';
        } else {
            errorMessage = updateEmail.response;
        }  
    };

    async function updatePasswordHandler() {
        if (password != passwordConfirm) {
            errorMessage = "Your passwords must match. Please enter a matching Password and Confirm Password combination.";
        } else if (passCheck != true){
            errorMessage = "Your passwords must be a strong password. It must contain at least one lowercase character, uppercase character, special character, and number.";
        } else {
            const variable = {};
            const query = `
                mutation userChangePassword($old_password: String = "", $new_password: String = "") {
                    user_change_password(arg: {old_password: $old_password, new_password: $new_password}) {
                        status
                        code
                    }
                }
            `;
            variable["old_password"] = passwordOld;
            variable["new_password"] = password;
            const accessToken = await token();
            const request = await fetch("http://localhost:8080/v1/graphql", {
                method: "POST",
                headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
                body: JSON.stringify({ query: query, variables: variable })
            });
            const updatePassword = await gqlResponseHandler(request);
            if (updatePassword.success === true){
                successMessage =  'Your password has been updated.';
            } else {
                errorMessage = 'There seems to be a problem with your request. Please ensure that your old password is correct. ' + updatePassword.response;
            }  
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
                            <input type="password" class="w-100 mb-xs" on:keyup={passwordStrengthCheck} on:change={passwordStrengthCheck} bind:value={password} placeholder="New Password..." />
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