-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-01-2024 a las 03:47:00
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pychat`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactos`
--

CREATE TABLE `contactos` (
  `contacto_id` int(11) NOT NULL,
  `contacto` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `contactos`
--

INSERT INTO `contactos` (`contacto_id`, `contacto`, `nombre`, `imagen`, `id_usuario`) VALUES
(6, 'magipoter@gmail.com', 'David', '2023205812_cubo.png', 7),
(7, 'magipoter777@gmail.com', 'Pedro Pistolas', '2023205827_cuboblack.jpeg', 6),
(8, 'magipoter@magipoter.com', 'Pablo Machetes', '2023205851_bad.jpeg', 6),
(8, 'magipoter@magipoter.com', 'Pablo Machetes', '2023205851_bad.jpeg', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `conversacion`
--

CREATE TABLE `conversacion` (
  `conversacion_id` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_contacto` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `conversacion`
--

INSERT INTO `conversacion` (`conversacion_id`, `id_usuario`, `id_contacto`) VALUES
(1, 6, 7),
(3, 6, 8),
(4, 7, 6),
(5, 7, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes`
--

CREATE TABLE `mensajes` (
  `mensajes_id` int(11) NOT NULL,
  `id_conversacion` int(11) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `mensaje` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensajes`
--

INSERT INTO `mensajes` (`mensajes_id`, `id_conversacion`, `id_usuario`, `mensaje`) VALUES
(1, 1, 6, 'Hola'),
(2, 1, 7, 'Holi crayoli');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `usuario_id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `imagen` varchar(255) NOT NULL,
  `edad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`usuario_id`, `nombre`, `correo`, `password`, `imagen`, `edad`) VALUES
(6, 'David', 'magipoter@gmail.com', 'scrypt:32768:8:1$VGvRN8h8tKKYrHSQ$7577bbf51eb616b9426a6e63980608566507eb8d9bb9ed49f2daf98b1c4e666059533b0c9ae07dce146fdceede9e4cf4fe1e70a1e215926310193fb0ac169b9d', '2023205812_cubo.png', 19),
(7, 'Pedro Pistolas', 'magipoter777@gmail.com', 'scrypt:32768:8:1$S7O1U42KLO2Dmh4v$a75f2dc7579733e4edde808835af8c33d99f7168cff3e0ad28bc848f5ed9f17e0f9a4aec7368ac95e69aafc2afa6d0f83f74767dcae48a9100f6d13c8e734467', '2023205827_cuboblack.jpeg', 23),
(8, 'Pablo Machetes', 'magipoter@magipoter.com', 'scrypt:32768:8:1$SksyULRI8KL4pek8$120546f454f6fe57d1e172cf7521d584f231912c26017dbdff39aae6296426a89bc5be175006f5682c115fbb7f19c65ebbad9df9b93648a1219a1623f0fb252c', '2023205851_bad.jpeg', 21),
(9, 'Segundo', 'si@si.si', 'scrypt:32768:8:1$x9zMxAX6iRXb5FNr$438076ea898531c304b2b378ccb00a429d91ecfee7049a7473f63d93e27ea575bb0bed4a641415ace7da43ea2299af6a6b40648bd9073078255593774a4349df', '2023205916_girasoles.jpg', 1003);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `conversacion`
--
ALTER TABLE `conversacion`
  ADD PRIMARY KEY (`conversacion_id`);

--
-- Indices de la tabla `mensajes`
--
ALTER TABLE `mensajes`
  ADD PRIMARY KEY (`mensajes_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`usuario_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `conversacion`
--
ALTER TABLE `conversacion`
  MODIFY `conversacion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `mensajes`
--
ALTER TABLE `mensajes`
  MODIFY `mensajes_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `usuario_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
