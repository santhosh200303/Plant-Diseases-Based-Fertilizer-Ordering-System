-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2024 at 08:32 PM
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fs`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `custreg`
--

CREATE TABLE `custreg` (
  `cust_id` int(50) NOT NULL,
  `custEmail` varchar(100) NOT NULL,
  `custPass` varchar(100) NOT NULL,
  `custRepass` varchar(100) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `custreg`
--

INSERT INTO `custreg` (`cust_id`, `custEmail`, `custPass`, `custRepass`, `date`) VALUES
(1, 'sakshi1001@gmail.com', 'sakshi', 'sakshi', '2024-11-16 16:36:50'),
(2, 'abc12@gmail.com', 'abc', 'abc', '2024-11-16 16:38:03'),
(3, 'amar12@gmail.com', 'amar', 'amar', '2024-11-16 16:42:15'),
(4, 'amar12@gmail.com', 'amar', 'amar', '2024-11-16 16:42:50'),
(5, 'johndoe@example.com', 'john', 'john', '2024-11-16 16:48:09'),
(6, 'janesmith@example.com', 'jane', 'jane', '2024-11-16 17:20:41'),
(7, 'mayur12@example.com', 'mayur', 'mayur', '2024-11-16 17:25:09');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `message` varchar(100) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `name`, `email`, `phone`, `message`, `date`) VALUES
(1, 'abc', 'abc@gmail.com', '7894561235', 'Good', '2024-11-16 08:42:48'),
(2, 'xyz', 'xyz@gmail.com', '7894561266', 'Very good', '2024-11-16 10:09:03');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(10) NOT NULL,
  `product_type` varchar(50) NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `product_desc` varchar(100) NOT NULL,
  `product_image` varchar(500) NOT NULL,
  `product_qty` int(10) NOT NULL,
  `product_rate` int(10) NOT NULL,
  `product_amt` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_type`, `product_name`, `product_desc`, `product_image`, `product_qty`, `product_rate`, `product_amt`) VALUES
(1, 'Fertilizer', 'Urea', 'Urea is the most important nitrogenous fertilizer in the country. ', 'Uera.jpg', 5, 800, 4000),
(2, 'Pesticide', 'Insecticides  ', 'Insecticides are substances used to mitigate insects of one or more species. ', 'insecticide.png', 5, 1200, 6000),
(3, 'Fertilizer', 'Potash', 'Potash includes various mined and manufactured salts that contain potassium in water-soluble form.', 'potash.png', 6, 800, 4000),
(4, 'Pesticide', 'Fumigants', 'Fumigants are extremely toxic gases used to protect stored products, especially grains, and to kill ', 'Fumigants.png', 5, 2000, 10000),
(5, 'Fertilizer', 'Compost  ', 'Rich in organic matter, improves soil structure and nutrient retention.', 'compost.png', 5, 1500, 7500);

-- --------------------------------------------------------

--
-- Table structure for table `purchase_order`
--

CREATE TABLE `purchase_order` (
  `purchase_id` int(100) NOT NULL,
  `Product_Name` varchar(100) NOT NULL,
  `Product_Price` int(100) NOT NULL,
  `Product_Qty` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchase_order`
--

INSERT INTO `purchase_order` (`purchase_id`, `Product_Name`, `Product_Price`, `Product_Qty`) VALUES
(1, 'Urea', 800, 1),
(2, 'Insecticides  ', 1200, 1),
(2, 'Potash', 800, 1);

-- --------------------------------------------------------

--
-- Table structure for table `purchase_transaction`
--

CREATE TABLE `purchase_transaction` (
  `purchase_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `purchase_id` int(100) NOT NULL,
  `Supplier_Name` varchar(100) NOT NULL,
  `Supplier_Mobile` varchar(100) NOT NULL,
  `Supplier_Address` varchar(100) NOT NULL,
  `Grand_Total` int(100) NOT NULL,
  `Pay_Mode` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchase_transaction`
--

INSERT INTO `purchase_transaction` (`purchase_date`, `purchase_id`, `Supplier_Name`, `Supplier_Mobile`, `Supplier_Address`, `Grand_Total`, `Pay_Mode`) VALUES
('2024-11-20 15:23:35', 1, 'Amar Patil', '7894561235', 'Kolhapur', 800, 'COD'),
('2024-11-20 15:53:27', 2, 'Rahul Kumar', '8956324176', 'Kolhapur', 2000, 'COD');

-- --------------------------------------------------------

--
-- Table structure for table `sale_order`
--

CREATE TABLE `sale_order` (
  `bill_no` int(100) NOT NULL,
  `Product_Name` varchar(100) NOT NULL,
  `Product_Price` int(100) NOT NULL,
  `Product_Qty` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sale_order`
--

INSERT INTO `sale_order` (`bill_no`, `Product_Name`, `Product_Price`, `Product_Qty`) VALUES
(1, 'Insecticides  ', 1200, 1);

-- --------------------------------------------------------

--
-- Table structure for table `sale_transaction`
--

CREATE TABLE `sale_transaction` (
  `bill_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `bill_no` int(50) NOT NULL,
  `Customer_Name` varchar(100) NOT NULL,
  `Customer_Mobile` varchar(100) NOT NULL,
  `Customer_Address` varchar(100) NOT NULL,
  `Grand_Total` int(100) NOT NULL,
  `Pay_Mode` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sale_transaction`
--

INSERT INTO `sale_transaction` (`bill_date`, `bill_no`, `Customer_Name`, `Customer_Mobile`, `Customer_Address`, `Grand_Total`, `Pay_Mode`) VALUES
('2024-11-20 17:58:36', 1, 'Sakshi Chechar', '7789451001', 'Kolhapur', 1200, 'COD');

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `supplier_id` int(10) NOT NULL,
  `supplier_name` varchar(50) NOT NULL,
  `supplier_email` varchar(50) NOT NULL,
  `supplier_mobileno` varchar(10) NOT NULL,
  `category` varchar(50) NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `supplier_address` varchar(100) NOT NULL,
  `supplier_GST` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `supplier_name`, `supplier_email`, `supplier_mobileno`, `category`, `product_name`, `supplier_address`, `supplier_GST`) VALUES
(1, 'Amar Patil', 'amar1@example.com', '7894561235', 'Fertilizer', 'Urea', 'Kolhapur', '22AAAAA0000A1Z5'),
(2, 'Ravi Shinde', 'ravi@example.com', '9632587415', 'Pesticide', 'Insecticides', 'Pune', '6935UYAA0000U65P'),
(3, 'Rahul Kumar', 'rahul@example.com', '8956324176', 'Fertilizer', 'Potash', 'Kolhapur', '55AAAAA0000A1Z5'),
(4, 'Umesh Patil', 'umesh@example.com', '7856124935', 'Pesticide', 'Fumigants', 'Kolhapur', '80AAAAA0000A1E5');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `custreg`
--
ALTER TABLE `custreg`
  ADD PRIMARY KEY (`cust_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `purchase_transaction`
--
ALTER TABLE `purchase_transaction`
  ADD PRIMARY KEY (`purchase_id`);

--
-- Indexes for table `sale_transaction`
--
ALTER TABLE `sale_transaction`
  ADD PRIMARY KEY (`bill_no`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `custreg`
--
ALTER TABLE `custreg`
  MODIFY `cust_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `purchase_transaction`
--
ALTER TABLE `purchase_transaction`
  MODIFY `purchase_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sale_transaction`
--
ALTER TABLE `sale_transaction`
  MODIFY `bill_no` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
