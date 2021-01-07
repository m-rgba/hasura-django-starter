<script>
    import { onMount } from "svelte";
    import { link } from "svelte-routing";
    import { token } from '../shared/auth.js'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    onMount(() => {
        getExpandedUser();
    });
    let pageRetry = 1;

    let successMessage;
    let errorMessage;

    let email = "";
    let newEmail = "";
    let role = "";
    export let username;

    let userVariable = {}
    let updateProfileVariable = {}

    async function getExpandedUser() {
        pageRetry = pageRetry + 1;
        if (pageRetry >= 15){
            errorMessage = 'Wasn\'t able to reconnect. Please refresh and try again.';
            throw 'JWT Refresh Error';
        }

        const accessToken = localStorage.getItem('token');
        const query = `
            query getUser($username : String!) {
                auth_user(where: {username: {_eq: $username}}) {
                    email
                    id
                    api_profile {
                        role
                    }
                }
            }
        `;
        userVariable["username"] = username;

        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
                Authorization: "Bearer " + accessToken,
            },
            body: JSON.stringify({
                query: query,
                variables: userVariable
            })
        });
        if (request.ok) {
            const response = await request.json();
            if (response.errors){
                if(response.errors[0].extensions.code === 'invalid-jwt'){ 
                    await new Promise(r => setTimeout(r, 500));
                    console.log('> Token Update / Reconnecting...');
                    token();
                    getExpandedUser();
                } else {
                    errorMessage = response.errors[0].message;
                }
            } else {
                pageRetry = 1;
                email = response.data.auth_user[0].email;
                newEmail = response.data.auth_user[0].email;
                role = response.data.auth_user[0].api_profile.role
            }
        } else {
            errorMessage = 'There was a problem with your request: ' + request.statusText;
        }
    }

    async function updateUserHandler() {
        pageRetry = pageRetry + 1;
        if (pageRetry >= 15){
            errorMessage = 'Wasn\'t able to reconnect. Please refresh and try again.';
            throw 'JWT Refresh Error';
        }

        const accessToken = localStorage.getItem('token');
        const query = `
            mutation updateUser($username: String!, $email: String!, $role: String!) {
                update_auth_user(where: {username: {_eq: $username}}, _set: {email: $email}){
                    affected_rows
                }
                update_api_profile(where: {auth_user: {username: {_eq: $username}}}, _set: {role: $role}) {
                    affected_rows
                }
            }
        `;
        updateProfileVariable["username"] = username;
        updateProfileVariable["email"] = newEmail;
        updateProfileVariable["role"] = role;

        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
                Authorization: "Bearer " + accessToken,
            },
            body: JSON.stringify({
                query: query,
                variables: updateProfileVariable
            })
        });
        if (request.ok) {
            const response = await request.json();
            if (response.errors){
                if(response.errors[0].extensions.code === 'invalid-jwt'){ 
                    await new Promise(r => setTimeout(r, 500));
                    console.log('> Token Update / Reconnecting...');
                    token();
                    updateUserHandler();
                } else {
                    errorMessage = response.errors[0].message;
                }
            } else {
                pageRetry = 1;
                successMessage = 'The user account has been updated.'
            }
        } else {
            errorMessage = 'There was a problem with your request: ' + request.statusText;
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
                <h1 class="mb-xs">{username}</h1>
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

                        <form on:submit|preventDefault={updateUserHandler}>
                            <p class="strong">Update Email</p>
                            <input type="email" class="w-100 mb-xs" bind:value={newEmail} placeholder="Update Email..." />

                            <p class="strong">Role</p>
                            <select bind:value={role} class="mb-xs w-100" name="roles">
                                <option disabled value="">Select a Role</option>
                                <option value="admin">Admin</option>
                                <option value="user">User</option>
                            </select>

                            <button type="submit" class="w-100 mb-xs">Update Profile</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</content>

<Footer />