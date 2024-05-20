# Import pydantic BaseSettigns module.
from pydantic_settings import BaseSettings

# Define the Settings class which inherits from BaseSettings
class Settings(BaseSettings):
    # Define properties corresponding to environment variables
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    admin_username: str
    admin_password: str

    secret_key: str
    jwt_algorithm: str
    access_token_expires_in: int
    refresh_token_expires_in: int
    #client_origin: str

    jwt_private_key: str
    jwt_public_key: str

    swagger_username: str
    swagger_password: str

    objects_folder: str
    nodes_folder: str
    queue_folder: str
    result_folder: str
    files_folder: str
    video_folder: str
    profile_image_folder: str

    # Define the Config inner class with the path to the environment file
    class Config:
        env_file = ".env"

# Create an instance of the Settings class
settings = Settings(
    database_hostname="localhost",
    database_username="postgres",
    database_password="postgres",
    database_name="anchorworld",
    database_port="5432",
    # database_username="admin",
    # database_password="admin",
    # database_port="3306",
    # database_name="superswing",
    # database_hostname="localhost",
    admin_username="admin",
    admin_password="admin",
    secret_key="cd67cdf09d9dc368960d7590e143b0d55c15f2d0da56b314b4a08a54aeca9b4b",
    jwt_algorithm="RS256",
    access_token_expires_in=1440,
    refresh_token_expires_in=86400,
    #client_origin="*",
    jwt_private_key="LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlCT2dJQkFBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVmlQWlJyVFpjd3l4RVhVRGpNaFZuCi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUUpBYm5LaENOQ0dOSFZGaHJPQ0RCU0IKdmZ2ckRWUzVpZXAwd2h2SGlBUEdjeWV6bjd0U2RweUZ0NEU0QTNXT3VQOXhqenNjTFZyb1pzRmVMUWlqT1JhUwp3UUloQU84MWl2b21iVGhjRkltTFZPbU16Vk52TGxWTW02WE5iS3B4bGh4TlpUTmhBaUVBbWRISlpGM3haWFE0Cm15QnNCeEhLQ3JqOTF6bVFxU0E4bHUvT1ZNTDNSak1DSVFEbDJxOUdtN0lMbS85b0EyaCtXdnZabGxZUlJPR3oKT21lV2lEclR5MUxaUVFJZ2ZGYUlaUWxMU0tkWjJvdXF4MHdwOWVEejBEWklLVzVWaSt6czdMZHRDdUVDSUVGYwo3d21VZ3pPblpzbnU1clBsTDJjZldLTGhFbWwrUVFzOCtkMFBGdXlnCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0t",
    jwt_public_key="LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZ3d0RRWUpLb1pJaHZjTkFRRUJCUUFEU3dBd1NBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVgppUFpSclRaY3d5eEVYVURqTWhWbi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==",
    swagger_username="swagger_user",
    swagger_password="swagger_password",

    objects_folder="C:/Users/USER/Desktop/anchorWorld_auth/objects",
    nodes_folder="C:/Users/USER/Desktop/anchorWorld_auth/nodes",
    queue_folder="C:/Users/USER/Desktop/anchorWorld_auth/queue",
    result_folder="C:/Users/USER/Desktop/anchorWorld_auth/results",
    files_folder="C:/Users/USER/Desktop/anchorWorld_auth/media_uploads",
    video_folder="C:/Users/USER/Desktop/anchorWorld_auth/videos",
    profile_image_folder="C:/Users/USER/Desktop/anchorWorld_auth/profile_image",
)

swagger_login_page = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Hacker Login Form</title>

    <style>
      @import url("https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap");
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: "Quicksand", sans-serif;
      }
      body {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: #000;
      }
      section {
        position: absolute;
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2px;
        flex-wrap: wrap;
        overflow: hidden;
      }
      section::before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background: linear-gradient(#000, #0f0, #000);
        animation: animate 5s linear infinite;
      }
      @keyframes animate {
        0% {
          transform: translateY(-100%);
        }
        100% {
          transform: translateY(100%);
        }
      }
      section span {
        position: relative;
        display: block;
        width: calc(6.25vw - 2px);
        height: calc(6.25vw - 2px);
        background: #181818;
        z-index: 2;
        transition: 1.5s;
      }
      section span:hover {
        background: #0f0;
        transition: 0s;
      }

      section .signin {
        position: absolute;
        width: 400px;
        background: #222;
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
        border-radius: 4px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 9);
      }
      section .signin .content {
        position: relative;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 40px;
      }
      section .signin .content h2 {
        font-size: 2em;
        color: #0f0;
        text-transform: uppercase;
      }
      section .signin .content .form {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 25px;
      }
      section .signin .content .form .inputBox {
        position: relative;
        width: 100%;
      }
      section .signin .content .form .inputBox input {
        position: relative;
        width: 100%;
        background: #333;
        border: none;
        outline: none;
        padding: 25px 10px 7.5px;
        border-radius: 4px;
        color: #fff;
        font-weight: 500;
        font-size: 1em;
      }
      section .signin .content .form .inputBox i {
        position: absolute;
        left: 0;
        padding: 15px 10px;
        font-style: normal;
        color: #aaa;
        transition: 0.5s;
        pointer-events: none;
      }
      .signin .content .form .inputBox input:focus ~ i,
      .signin .content .form .inputBox input:valid ~ i {
        transform: translateY(-7.5px);
        font-size: 0.8em;
        color: #fff;
      }
      .signin .content .form .links {
        position: relative;
        width: 100%;
        display: flex;
        justify-content: space-between;
      }
      .signin .content .form .links a {
        color: #fff;
        text-decoration: none;
      }
      .signin .content .form .links a:nth-child(2) {
        color: #0f0;
        font-weight: 600;
      }
      .signin .content .form .inputBox input[type="submit"] {
        padding: 10px;
        background: #0f0;
        color: #000;
        font-weight: 600;
        font-size: 1.35em;
        letter-spacing: 0.05em;
        cursor: pointer;
      }
      input[type="submit"]:active {
        opacity: 0.6;
      }
      @media (max-width: 900px) {
        section span {
          width: calc(10vw - 2px);
          height: calc(10vw - 2px);
        }
      }
      @media (max-width: 600px) {
        section span {
          width: calc(20vw - 2px);
          height: calc(20vw - 2px);
        }
      }
    </style>
  </head>
  <body>
    <!-- partial:index.partial.html -->
    <!DOCTYPE html>

    <html lang="en">
      <head>
        <meta charset="UTF-8" />

        <title>CodePen - Animated Login Form using Html &amp; CSS Only</title>
      </head>

      <body>
        <!-- partial:index.partial.html -->

        <section>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>
          <span></span> <span></span> <span></span> <span></span> <span></span>

          <div class="signin">
            <div class="content">
              <h2>Sign In</h2>

              <form class="form" id="loginForm">
                <div class="inputBox">
                  <input type="text" id="username" required /> <i>Username</i>
                </div>

                <div class="inputBox">
                  <input type="password" id="password" required /> <i>Password</i>
                </div>

                <div class="links">
                  <p id="message" style="color: #0f0;"></p>
                </div>

                <div class="inputBox">
                  <input type="submit" value="Login" />
                </div>
              </form>
            </div>
          </div>
        </section>
        <!-- partial -->
      </body>
    </html>
    <!-- partial -->
  </body>
  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const loginForm = document.getElementById("loginForm");
      const message = document.getElementById("message");

      loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const data = {
          username,
          password,
        };

        try {
          const response = await fetch(
            "/api/auth/login",
            {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
            }
          );

          const responseData = await response.json();
          // console.log(responseData)
          if (response.ok) {
          
            fetch("/api/auth/me")
              .then((userDataResponse) => {
                if (userDataResponse.ok) {
                  return userDataResponse.json();
                } else {
                  throw new Error("Failed to fetch user data");
                }
              })
              .then((userData) => {
                if (userData.is_admin) {
                  // Redirect if the user is an admin
                  location.replace("/api/docs");
                } else {
                  // Redirect to the regular user page
                  message.textContent = "you are not admin";
                }
              })
              .catch((error) => {
                message.textContent = "Something is wrong";
              });
          } else {
            message.textContent = "Login failed. Please check your credentials.";
          }
        } catch (error) {
          console.error("Error:", error);
          message.textContent = "An error occurred.";
        }
      });
    });
  </script>
</html>
"""