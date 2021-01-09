<script>
    import { onMount } from "svelte";
    import { link } from "svelte-routing";
    import { token } from '../shared/auth.js'
    import { gqlResponseHandler } from '../shared/requests.js'

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    let urlParams = new URLSearchParams(window.location.search);
    let userCreated = urlParams.get("created") == "true";
    let userUpdated = urlParams.get("updated") == "true";

    let successMessage;
    let errorMessage;

    let searchQuery;
    let users;
    let usersReady;
    let userRole = localStorage.getItem("user_role");

    onMount(() => {
        if (userRole === 'admin' || userRole === 'manager'){
            getUsers();
        }
        getQueryMsgs();
    });

    async function getQueryMsgs() {
        if(userCreated === true) {
            successMessage = "A new user has been successfully created."
        } else if(userUpdated === true) {
            successMessage = "A user has been successfully updated."
        }
    }

    async function userStatusChange(statusType, id) {
        const variable = {};
        const query = `
            mutation updateUserStatus($userID: Int!, $statusType: Boolean!) {
                    update_auth_user(where: {id: {_eq: $userID}}, _set: {is_active: $statusType}) {
                        returning {
                            username
                        }
                    }
                }
        `;
        variable["statusType"] = statusType;
        variable["userID"] = id;
        const accessToken = await token();
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const userChange = await gqlResponseHandler(request);
        if (userChange.success === true){
            successMessage = 'Account status has been updated.'
            getUsers();
        } else {
            errorMessage = userChange.response;
        }  
    };

    async function getUsers() {
        const variable = {};
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
        if (searchQuery === ''){ variable["searchQuery"] = null; } else { variable["searchQuery"] = searchQuery; }
        const accessToken = await token();
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const userList = await gqlResponseHandler(request);
        if (userList.success === true){
            users = userList.response.auth_user;
            usersReady = 1;
        } else {
            errorMessage = userList.response;
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
            <div class="col-12 mb-sm">
                <h1>Users</h1>
            </div>
            <div class="col-12">
                    {#if userRole === "admin" || userRole === "manager"}
                        <div class="card">
                            <div class="pad flex-center">
                                <a use:link href="/user/create"><button class="primary" style="">Create User</button></a>
                                <input style="width:240px; margin-left:auto;" class="mr-xxs" bind:value={searchQuery} placeholder="Search..." /> <button on:click="{getUsers}">Search</button>
                            </div>

                            <style>
                                .tbl-inspect{
                                    width:32px;
                                }
                                .tbl-disable{
                                    width:98px;
                                }
                            </style>

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
                                    {:else}
                                        <!-- Table Placeholders -->
                                        <tr>
                                            <td class="actions tbl-inspect">
                                            </td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td><span class="placeholder">***************</span></td>
                                            <td><span class="placeholder">*********</span></td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td class="actions tbl-disable"></td>
                                        </tr>
                                        <tr>
                                            <td class="actions tbl-inspect">
                                            </td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td><span class="placeholder">***************</span></td>
                                            <td><span class="placeholder">*********</span></td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td class="actions tbl-disable"></td>
                                        </tr>
                                        <tr>
                                            <td class="actions tbl-inspect">
                                            </td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td><span class="placeholder">***************</span></td>
                                            <td><span class="placeholder">*********</span></td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td class="actions tbl-disable"></td>
                                        </tr>
                                        <tr>
                                            <td class="actions tbl-inspect">
                                            </td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td><span class="placeholder">***************</span></td>
                                            <td><span class="placeholder">*********</span></td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td class="actions tbl-disable"></td>
                                        </tr>
                                        <tr>
                                            <td class="actions tbl-inspect">
                                            </td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td><span class="placeholder">***************</span></td>
                                            <td><span class="placeholder">*********</span></td>
                                            <td><span class="placeholder">***********</span></td>
                                            <td class="actions tbl-disable"></td>
                                        </tr>
                                    {/if}
                                </tbody>
                            </table>    
                        </div>
                    {:else}
                        Sign into Hasura (<a target="_new" href="http://localhost:8080/console/data/schema/public">http://localhost:8080/console/data/schema/public</a>) and set your user profile status as <strong>admin</strong> or <strong>manager</strong> (through the <strong>api_profile table</strong>).
                    {/if}

            </div>
        </div>
    </div>
</content>

<Footer />