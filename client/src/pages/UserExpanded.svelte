<script>
    import { onMount } from "svelte";
    import { navigate, link } from "svelte-routing";
    import { token } from '../shared/auth.js'
    import { gqlResponseHandler } from '../shared/requests.js'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    onMount(() => {
        getExpandedUser();
    });
    let successMessage;
    let errorMessage;

    let email = "";
    let newEmail = "";
    let role = "";
    let is_active = "";

    export let username;

    async function getExpandedUser() {
        const variable = {};
        const query = `
            query getUser($username : String!) {
                auth_user(where: {username: {_eq: $username}}) {
                    email
                    is_active
                    api_profile {
                        api_role{
                            id
                            name
                        }
                        uuid
                    }
                }
            }
        `;
        variable["username"] = username;
        const accessToken = await token();
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const userProfile = await gqlResponseHandler(request);
        if (userProfile.success === true){
            is_active = userProfile.response.auth_user[0].is_active;
            email = userProfile.response.auth_user[0].email;
            role = userProfile.response.auth_user[0].api_profile.api_role.id;
        } else {
            errorMessage = userProfile.response;
        }  
    };

    async function userStatusChange(statusType) {
        const variable = {};
        const query = `
            mutation updateUserStatus($username: String!, $statusType: Boolean!) {
                update_auth_user(where: {username: {_eq: $username}}, _set: {is_active: $statusType}) {
                    returning {
                        username
                    }
                }
            }
        `;
        variable["username"] = username;
        variable["statusType"] = statusType;
        const accessToken = await token();
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const userStatus = await gqlResponseHandler(request);
        if (userStatus.success === true){
            is_active = statusType;
            successMessage = "The user\'s status has been updated."
        } else {
            errorMessage = userStatus.response;
        }  
    };

    async function updateUserHandler() {
        const variable = {};
        const query = `
            mutation updateUser($username: String!, $email: String!, $roleID: bigint!) {
                update_auth_user(where: {username: {_eq: $username}}, _set: {email: $email}) {
                    affected_rows
                }
                update_api_profile(where: {auth_user: {username: {_eq: $username}}}, _set: {role_id: $roleID}) {
                    affected_rows
                }
            }
        `;
        variable["username"] = username;
        if (newEmail === ''){ variable["email"] = email; } else { variable["email"] = newEmail; }
        variable["roleID"] = role;
        const accessToken = await token();
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const userProfile = await gqlResponseHandler(request);
        if (userProfile.success === true){
            navigate("/users?updated=true", { replace: true });
        } else {
            errorMessage = userProfile.response;
        }  
    };
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
                        <p class="strong">Current Status</p>
                        {#if is_active === true}
                            <input class="w-100 mb-xs" disabled value="Active" />
                        {:else}
                            <input class="w-100 mb-xs" disabled value="Disabled" />
                        {/if}

                        <form on:submit|preventDefault={updateUserHandler}>
                            <p class="strong">Update Email</p>
                            <input type="email" class="w-100 mb-xs" bind:value={newEmail} placeholder="Update Email..." />

                            <p class="strong">Role</p>
                            <select bind:value={role} class="mb-xs w-100" name="roles">
                                <option disabled value="">Select a Role</option>
                                <option value="2">Manager</option>
                                <option value="1">User</option>
                            </select>

                            <button type="submit" class="w-100 mb-xs">Update Profile</button>
                        </form>
                    </div>
                </div>
                {#if is_active === true}
                    <a class="red" on:click={() => userStatusChange(false)} href="#!"><ion-icon name="close-circle-outline"></ion-icon> Disable User</a>
                {:else}
                    <a class="green" on:click={() => userStatusChange(true)} href="#!"><ion-icon name="checkmark-circle-outline"></ion-icon> Enable User</a>
                {/if}
            </div>
        </div>
    </div>
</content>

<Footer />