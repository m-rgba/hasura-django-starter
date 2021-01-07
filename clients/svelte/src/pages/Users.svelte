<script>
    import { onMount } from "svelte";
    import { link } from "svelte-routing";
    import { token } from '../shared/auth.js'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    onMount(() => {
        if (userRole === 'admin'){
            getUsers();
        }
        getQueryMsgs();
    });
    let pageRetry = 1;

    // Check QueryStrings from Alert
    let urlParams = new URLSearchParams(window.location.search);
    let userCreated = urlParams.get("created") == "true";

    let successMessage;
    let errorMessage;

    let users;
    let usersReady;

    let userRole = localStorage.getItem("user_role");

    let searchQuery;

    let searchVariables = {};
    let userStatusVariables = {};

    async function getQueryMsgs() {
        if(userCreated === true) {
            successMessage = "A new user has been created."
        }
    }

    // TODO: Getting a little lazy here > just running getUsers again vs updating the affected records only which can be returned via this query.
    async function userStatusChange(statusType, id) {
        pageRetry = pageRetry + 1;
        if (pageRetry >= 15){
            errorMessage = 'Wasn\'t able to reconnect. Please refresh and try again.';
            throw 'JWT Refresh Error';
        }

        const accessToken = localStorage.getItem('token');
        const query = `
            mutation updateUserStatus($userID: Int!, $statusType: Boolean!) {
                    update_auth_user(where: {id: {_eq: $userID}}, _set: {is_active: $statusType}) {
                        returning {
                            username
                        }
                    }
                }
        `;

        userStatusVariables["statusType"] = statusType;
        userStatusVariables["userID"] = id;

        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
                Authorization: "Bearer " + accessToken,
            },
            body: JSON.stringify({
                query: query,
                variables: userStatusVariables
            })
        });
        if (request.ok) {
            const response = await request.json();
            if (response.errors){
                if(response.errors[0].extensions.code === 'invalid-jwt'){ 
                    await new Promise(r => setTimeout(r, 500));
                    console.log('> Token Update / Reconnecting...');
                    token();
                    userStatusChange(statusType, id);
                } else {
                    errorMessage = response.errors[0].message;
                }
            } else {
                const userUpdated = response.data.update_auth_user.returning[0].username;
                if (statusType === true){
                    successMessage = userUpdated + '\'s profile has been enabled.'
                } else {
                    successMessage = userUpdated + '\'s profile has been disabled.'
                }
                getUsers();
                pageRetry = 1;
            }
        } else {
            errorMessage = 'There was a problem with your request: ' + request.statusText;
        }
        await new Promise(r => setTimeout(r, 500));
    }

    async function getUsers() {
        pageRetry = pageRetry + 1;
        if (pageRetry >= 15){
            errorMessage = 'Wasn\'t able to reconnect. Please refresh and try again.';
            throw 'JWT Refresh Error';
        }
        const accessToken = localStorage.getItem('token');
        const query = `
            query allUsers($searchQuery: String) {
                auth_user(where: {_or: [{username: {_ilike: $searchQuery}}, {email: {_ilike: $searchQuery}}]}) {
                    id
                    username
                    email
                    is_active
                    api_profile {
                        role
                        uuid
                    }
                }
            }
        `;
        if (searchQuery === ''){
            searchVariables["searchQuery"] = null;
        } else {
            searchVariables["searchQuery"] = searchQuery;
        }

        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
                Authorization: "Bearer " + accessToken,
            },
            body: JSON.stringify({
                query: query,
                variables: searchVariables
            })
        });
        if (request.ok) {
            const response = await request.json();
            if (response.errors){
                if(response.errors[0].extensions.code === 'invalid-jwt'){ 
                    await new Promise(r => setTimeout(r, 500));
                    console.log('> Token Update / Reconnecting...');
                    token();
                    getUsers();
                } else {
                    errorMessage = response.errors[0].message;
                }
            } else {
                users = response.data.auth_user;
                usersReady = 1;
                pageRetry = 1;
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
            <div class="col-12 mb-sm">
                <h1>Users</h1>
            </div>
            <div class="col-12">
                    <div class="card">
                        {#if userRole === "admin"}
                            <div class="pad flex-center">
                                <a use:link href="/user/create"><button class="primary" style="">Create User</button></a>
                                <input style="width:240px; margin-left:auto;" class="mr-xxs" bind:value={searchQuery} placeholder="Search..." /> <button on:click="{getUsers}">Search</button>
                            </div>
                        {/if}

                        <style>
                            .tbl-inspect{
                                width:32px;
                            }
                            .tbl-disable{
                                width:98px;
                            }
                        </style>

                        {#if userRole === "admin"}
                            <table>
                                <thead>
                                    <tr>
                                        <th class="inspect tbl-inspect"></th>
                                        <th>Username</th>
                                        <th>Email</th>
                                        <th>Role</th>
                                        <th>Status</th>
                                        <th class="actions tbl-disable"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#if usersReady === 1}
                                        {#each users as user}
                                            <tr>
                                                <td class="actions tbl-inspect">
                                                    <a class="muted" use:link href="/user/{user.username}"><ion-icon style="font-size:16px;" name="search-outline"></ion-icon></a>
                                                </td>
                                                <td><a use:link href="/user/{user.username}">{user.username}</a></td>
                                                <td>{user.email}</td>
                                                <td>{user.api_profile.role}</td>
                                                {#if user.is_active === true}
                                                    <td><span class="badge positive">Active</span></td>
                                                    <td class="actions tbl-disable">
                                                        <button on:click={() => userStatusChange(false, user.id)} class="red sm"><ion-icon style="font-size:16px;" name="close-circle-outline"></ion-icon> Disable</button>
                                                    </td>
                                                {:else}
                                                    <td><span class="badge negative">Disabled</span></td>
                                                    <td class="actions tbl-disable">
                                                        <button on:click={() => userStatusChange(true, user.id)} class="sm"><ion-icon style="font-size:16px;" name="checkmark-circle-outline"></ion-icon> Enable</button>
                                                    </td>
                                                {/if}
                                            </tr>
                                        {/each}
                                    {/if}
                                </tbody>
                            </table>
                        {:else}
                            <div class="pad">Sign into Hasura (http://localhost:8080/console/data/schema/public) and set your user profile status as admin (through the api_profile table).</div>
                        {/if}
                    </div>
            </div>
        </div>
    </div>
</content>

<Footer />