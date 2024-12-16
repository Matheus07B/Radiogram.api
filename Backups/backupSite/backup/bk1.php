<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Página inicial com links para login e registro.">
  <title>Página Inicial</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .container {
      text-align: center;
      background: #ffffff;
      padding: 20px 40px;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .container h1 {
      margin-bottom: 20px;
      color: #333333;
    }
    .container a {
      display: inline-block;
      margin: 10px 20px;
      padding: 10px 20px;
      text-decoration: none;
      color: #ffffff;
      background-color: #007BFF;
      border-radius: 5px;
      font-size: 16px;
      transition: background-color 0.3s ease;
    }
    .container a:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Bem-vindo!</h1>
    <p>Escolha uma das opções abaixo para continuar:</p>
    <a href="login/">Login</a>
    <a href="register/">Registrar</a>
  </div>
</body>
</html>
