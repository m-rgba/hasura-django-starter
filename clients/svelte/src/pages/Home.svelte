<script>
    import { onMount } from "svelte";

    // Components
    import Header from "../components/Header.svelte"
    import Footer from "../components/Footer.svelte"
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

<content>
    <div id="chat-container" class="container pt-xl">
        <div class="row mb-sm">
            <div class="col-3"> </div>
            <div class="col-6">
                <h1 class="mb-xs">Realtime Test</h1>
                <p><ion-icon name="arrow-back"></ion-icon> Back to Users</p>
            </div>
        </div>
        <div class="row">
            <div class="col-3"> </div>
            <div class="col-6 mb-sm">

                <div class="messages">

                    <div class="row mb-sm">
                        <div class="col-10">
                            <div class="card pad other-message">
                                <p><strong>System</strong></p>
                                <p>Hi there! Give it a try, send your first message.</p>
                            </div>
                        </div>
                    </div>

                    <div class="row mb-sm">
                        <div class="col-10">
                            <div class="card pad other-message">
                                <p><strong>Username</strong> <span class="pull-right">Post time</span></p>
                                <p>Other message</p>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-2"></div>
                        <div class="col-10">
                            <div class="card pad my-message">
                                <p><strong>Username</strong> <span class="pull-right">Post time</span></p>
                                <p>My message</p>
                            </div>
                        </div>
                    </div>

                </div>

                <div id="message-box" class="card pad shadow">
                    <div class="input mb-xs w-100" role="textbox" placeholder="Enter your message here..." contenteditable=true>                        
                    </div>
                    <div class="right">
                        <button class="primary">Send Message</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</content>


<div id="footer-mobile">
    <Footer />
</div>