 <script>
	import  axios  from 'axios';
    import {url, redirect} from "@roxi/routify"
     let email = "";
     let password = "";

     const handleSubmit =  async ()=> {
         try {
             const user = await axios.post("http://127.0.0.1:8000/api/v1/login", {
                 "email":email,
                 "password":password
             })
             if(user.status == 200){
                 let {message, user} = user.data.message
                 alert(`${message} ${user.firstname}`)
             }
             
         } catch (error) {
             
         }
       
     }

     
 </script>







<div class="login">
    <div class="container sm:px-10">
        <div class="block xl:grid grid-cols-2 gap-4">
         
            <div class="hidden xl:flex flex-col min-h-screen">
                <a href="/" class="-intro-x flex items-center pt-5">
                    <img alt="Midone Tailwind HTML Admin Template" class="w-6" src="dist/images/logo.svg">
                    <span class="text-white text-lg ml-3"> Mid<span class="font-medium">One</span> </span>
                </a>
                <div class="my-auto">
                    <img alt="Midone Tailwind HTML Admin Template" class="-intro-x w-1/2 -mt-16" src="dist/images/illustration.svg">
                    <div class="-intro-x text-white font-medium text-4xl leading-tight mt-10">
                        A few more clicks to 
                        <br>
                        sign in to your account.
                    </div>
                    <div class="-intro-x mt-5 text-lg text-white dark:text-gray-500">Manage all your e-commerce accounts in one place</div>
                </div>
            </div>

            <div class="h-screen xl:h-auto flex py-5 xl:py-0 my-10 xl:my-0">
                <div class="my-auto mx-auto xl:ml-20 bg-white xl:bg-transparent px-5 sm:px-8 py-8 xl:p-0 rounded-md shadow-md xl:shadow-none w-full sm:w-3/4 lg:w-2/4 xl:w-auto">
                    <h2 class="intro-x font-bold text-2xl xl:text-3xl text-center xl:text-left">
                        Sign In
                    </h2>
                    <div class="intro-x mt-2 text-gray-500 xl:hidden text-center">A few more clicks to sign in to your account. Manage all your e-commerce accounts in one place</div>
                    <div class="intro-x mt-8">
                        <input required bind:value="{email}" type="text" class="intro-x login__input input input--lg border border-gray-300 block" placeholder="Email">
                        <input required bind:value="{password}" type="password" class="intro-x login__input input input--lg border border-gray-300 block mt-4" placeholder="Password">
                    </div>
                    <div class="intro-x flex text-gray-700 dark:text-gray-600 text-xs sm:text-sm mt-4">
                        <a href="{$url("/")}">Forgot Password?</a> 
                    </div>
                    <div class="intro-x mt-5 xl:mt-8 text-center xl:text-left">
                        <button class="button button--lg w-full xl:w-32 text-white bg-theme-1 xl:mr-3 align-top" on:click="{handleSubmit}">Login</button>
                        <a href="{$url("/register")}"><button class="button button--lg w-full xl:w-32 text-gray-700 border border-gray-300 dark:border-dark-5 dark:text-gray-300 mt-3 xl:mt-0 align-top">Sign up</button></a>
                    </div>
                    <div class="intro-x mt-10 xl:mt-24 text-gray-700 dark:text-gray-600 text-center xl:text-left">
                        By signin up, you agree to our 
                        <br>
                        <a class="text-theme-1 dark:text-theme-10" href="/">Terms and Conditions</a> & <a class="text-theme-1 dark:text-theme-10" href="">Privacy Policy</a> 
                    </div>
                </div>
            </div>
            
        </div>
    </div>
    
</div>