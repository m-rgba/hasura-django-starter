<script>
    import { onMount } from "svelte";
    import moment from 'moment';
    import { token } from '../shared/auth.js'
    import { gqlResponseHandler } from '../shared/requests.js'

    // Apollo
    import ApolloClient from 'apollo-client';
    import { client } from '../shared/apollo.js'
	import { setClient } from 'svelte-apollo';
    import { subscribe, query } from 'svelte-apollo';
    import gql from 'graphql-tag';

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"

    let user_role = localStorage.getItem("user_role");
    let username = localStorage.getItem("user_name");
    let user_id = localStorage.getItem("user_id");

    let message;

    let successMessage;
    let errorMessage;

    setClient(client);
    const MESSAGES = gql`
        subscription realtimeMsgs {
        demo_realtime {
                message
                created_by
                created_at
                auth_user {
                    username
                }
            }
        }
    `;
    const messageSubscribe = subscribe(client, { query: MESSAGES });

    async function sendMessage() {
        let query;
        const variable = {};
        // Other users are restricted for defining their own 'created_by' > added so the feature doesn't break for Hasura Admins (which dont auto-populate).
        if(user_role === "admin"){
            query = `
                mutation updateUserStatus($message: String!, $created_by: Int) {
                    insert_demo_realtime_one(object: {created_by: $created_by, message: $message}) {
                        created_at
                        message
                    }
                }
            `; 
        } else {
            query = `
                mutation updateUserStatus($message: String!) {
                    insert_demo_realtime_one(object: {message: $message}) {
                        created_at
                        message
                    }
                }
            `; 
        }
        if(user_role === "admin"){
            variable["created_by"] = user_id;
        }
        variable["message"] = message;
        const accessToken = await token();
        const request = await fetch("http://localhost:8080/v1/graphql", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: "Bearer " + accessToken, },
            body: JSON.stringify({ query: query, variables: variable })
        });
        const sendMessage = await gqlResponseHandler(request);
        if (sendMessage.success === true){
            console.log("> Message sent");
            // console.log(sendMessage.response);
        } else {
            errorMessage = sendMessage.response;
        }  
    };
</script>

<style>
    #chat-container{
        margin-bottom: 166px;
    }
    #message-box{
        position: fixed;
        width:50%;
        left:50%;
        bottom: 58px;
        transform: translate(-50%, 0);
    }
    .my-message{
        border:0;
        background: #1D4ED8;
        color:#fff;
    }
    .other-message{
        border:0;
        background: #E5E7EB;
    }

    @media (max-width: 768px) {                                
        #message-box{
            width:95%;
            bottom: 16px;
        }
        #footer-mobile{
            display: none;
        }
    }
</style>

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
    <div id="chat-container" class="container pt-xl">
        <div class="row mb-sm">
            <div class="col-3"> </div>
            <div class="col-6">
                <h1 class="mb-xs">Realtime Demo</h1>
                <p class="muted">This is a demonstration of the realtime capabilities of Hasura's GraphQL API.</p>
                <p class="muted">Send a message as another account and you'll be able to see messages stream in.</p>
                <p class="muted">On the client side we're using svelte-apollo to display the results.</p>
            </div>
        </div>
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6 mb-sm">

                <div class="messages">

                    {#await $messageSubscribe}
                    <div class="row mb-sm">
                        <div class="col-10">
                            <div class="card pad other-message">
                                <p><span class="placeholder">***************</span></p>
                                <p><span class="placeholder">********** ***** **********</span></p>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-sm">
                        <div class="col-10">
                            <div class="card pad other-message">
                                <p><span class="placeholder">***************</span></p>
                                <p><span class="placeholder">********** ***** **********</span></p>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-sm">
                        <div class="col-10">
                            <div class="card pad other-message">
                                <p><span class="placeholder">***************</span></p>
                                <p><span class="placeholder">********** ***** **********</span></p>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-sm">
                        <div class="col-10">
                            <div class="card pad other-message">
                                <p><span class="placeholder">***************</span></p>
                                <p><span class="placeholder">********** ***** **********</span></p>
                            </div>
                        </div>
                    </div>

                    {:then $messageSubscribe}
                        <div class="row mb-sm">
                            <div class="col-10">
                                <div class="card pad other-message">
                                    <p><strong>System</strong></p>
                                    <p>Hi there! Give it a try, send your first message.</p>
                                </div>
                            </div>
                        </div>

                        {#each $messageSubscribe.data.demo_realtime as message}
                            {#if message.auth_user[0].username === username}
                                <div class="row mb-sm">
                                    <div class="col-2"></div>
                                    <div class="col-10">
                                        <div class="card pad my-message">
                                            <p><strong>{message.auth_user[0].username}</strong> <span class="pull-right" style="opacity:0.7">{moment(message.created_at).format('lll')}</span></p>
                                            <p>{message.message}</p>
                                        </div>
                                    </div>
                                </div>
                            {:else}
                                <div class="row mb-sm">
                                    <div class="col-10">
                                        <div class="card pad other-message">
                                            <p><strong>{message.auth_user[0].username}</strong> <span class="pull-right" style="opacity:0.7">{moment(message.created_at).format('lll')}</span></p>
                                            <p>{message.message}</p>
                                        </div>
                                    </div>
                                </div>
                            {/if}
                    {/each}                    
                    {:catch error}
                        {JSON.stringify(error)}
                    {/await}
                </div>

                <div id="message-box" class="card pad shadow">
                    <form on:submit|preventDefault={sendMessage}>
                        <div class="input mb-xs w-100" role="textbox" bind:innerHTML={message} placeholder="Enter your message here..." contenteditable=true>                        
                        </div>
                        <div class="right">
                            <button class="primary">Send Message</button>
                        </div>
                    </form>
                </div>
                
            </div>
        </div>

    </div>
</content>


<div id="footer-mobile">
    <Footer />
</div>