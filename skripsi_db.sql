-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 01, 2020 at 06:18 AM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `skripsi_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `beritasum_indikator`
--

CREATE TABLE `beritasum_indikator` (
  `waktu` date NOT NULL,
  `indikator` varchar(32) NOT NULL,
  `jumlah` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `beritasum_sumber`
--

CREATE TABLE `beritasum_sumber` (
  `waktu` date NOT NULL,
  `sumber` varchar(10) NOT NULL,
  `jumlah` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `berita_detail`
--

CREATE TABLE `berita_detail` (
  `id_berita` int(11) NOT NULL,
  `judul` varchar(120) NOT NULL,
  `waktu` date NOT NULL,
  `tag` text NOT NULL,
  `isi` text CHARACTER SET utf8mb4 NOT NULL,
  `sumber` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `indikator_ref`
--

CREATE TABLE `indikator_ref` (
  `id_indikator` varchar(6) NOT NULL,
  `indikator_utama` varchar(7) NOT NULL,
  `indikator` varchar(32) NOT NULL,
  `sub_indikator` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `indikator_ref`
--

INSERT INTO `indikator_ref` (`id_indikator`, `indikator_utama`, `indikator`, `sub_indikator`) VALUES
('IND001', 'Ekonomi', 'Ekspor-Impor', 'Indeks Unit Value Ekspor/Impor'),
('IND002', 'Ekonomi', 'Indeks Harga Perdagangan Besar', 'Indeks Harga Perdagangan Besar (IHPB)'),
('IND003', 'Ekonomi', 'Inflasi', 'Indeks Harga Konsumen (IHK)'),
('IND004', 'Ekonomi', 'Inflasi', 'Inflasi'),
('IND005', 'Ekonomi', 'Inflasi', 'Indeks Konsumsi Rumah Tangga (IKRT) '),
('IND006', 'Ekonomi', 'Inflasi', 'Inflasi Perdesaan'),
('IND007', 'Ekonomi', 'Indeks Tendensi Bisnis', 'Indeks Tendensi Bisnis (ITB) '),
('IND008', 'Ekonomi', 'Indeks Tendensi Bisnis', 'Indeks Indikator Kini (IIK) '),
('IND009', 'Ekonomi', 'Indeks Tendensi Bisnis', 'Indeks Indikator Mendatang (IIM)'),
('IND010', 'Ekonomi', 'Indeks Tendensi Konsumen', 'Indeks Tendensi Konsumen (ITK)'),
('IND011', 'Ekonomi', 'Indeks Tendensi Konsumen', 'Indeks Indikator Kini (IIK)'),
('IND012', 'Ekonomi', 'Indeks Tendensi Konsumen', 'Indeks Indikator Mendatang (IIM)'),
('IND013', 'Ekonomi', 'Nilai Tukar Petani', 'Nilai Tukar Petani (NTP)'),
('IND014', 'Ekonomi', 'Nilai Tukar Petani', 'Indeks Harga yang Diterima Petani (It)'),
('IND015', 'Ekonomi', 'Nilai Tukar Petani', 'Indeks Harga yang Dibayar Petani (Ib)'),
('IND016', 'Ekonomi', 'Nilai Tukar Petani', 'Rata-Rata Harga Gabah'),
('IND017', 'Ekonomi', 'Pariwisata', 'Rata-Rata Lama Menginap Tamu (Asing dan Dalam Negeri)'),
('IND018', 'Ekonomi', 'Pariwisata', 'Rata-Rata Lama Tinggal Wisatawan Mancanegara'),
('IND019', 'Ekonomi', 'Pariwisata', 'Rata-Rata Pengeluaran per Wisman per Hari per Kunjungan'),
('IND020', 'Ekonomi', 'Pariwisata', 'Tingkat Penghunian Kamar (TPK)'),
('IND021', 'Ekonomi', 'Pariwisata', 'Penerimaan dari Wisatawan Mancanegara'),
('IND022', 'Ekonomi', 'PDB/PDRB', 'Produk Domestik Bruto (PDB)/Produk Domestik Regional Bruto (PDRB)'),
('IND023', 'Ekonomi', 'PDB/PDRB', 'Laju Pertumbuhan PDB/PDRB '),
('IND024', 'Ekonomi', 'PDB/PDRB', 'Indeks Implisit '),
('IND025', 'Ekonomi', 'PDB/PDRB', 'Distribusi Persentase PDB/PDRB '),
('IND026', 'Ekonomi', 'PDB/PDRB', 'PDB/PDRB per Kapita '),
('IND027', 'Ekonomi', 'PDB/PDRB', 'Rasio Modal-Output Marginal '),
('IND028', 'Ekonomi', 'PDB/PDRB', 'Rasio Tenaga Kerja-Output Marginal'),
('IND029', 'Ekonomi', 'Pertumbuhan Produksi Industri', 'Pertumbuhan Produksi Industri Pengolahan '),
('IND030', 'Ekonomi', 'Pertumbuhan Produksi Industri', 'Indeks Produksi Industri Pengolahan '),
('IND031', 'Ekonomi', 'Transportasi', 'Rasio Penumpang per Pesawat Udara '),
('IND032', 'Ekonomi', 'Transportasi', 'Rasio Barang per Pesawat Udara '),
('IND033', 'Ekonomi', 'Transportasi', 'Rasio Penumpang per Kapal '),
('IND034', 'Ekonomi', 'Transportasi', 'Rasio Barang per Kapal '),
('IND035', 'Ekonomi', 'Transportasi', 'Rasio Penduduk terhadap Mobil Penumpang '),
('IND036', 'Ekonomi', 'Transportasi', 'Rasio Penduduk terhadap Kendaraan Bermotor '),
('IND037', 'Ekonomi', 'Transportasi', 'Rasio Penduduk terhadap Bus Umum '),
('IND038', 'Ekonomi', 'Transportasi', 'Jumlah Kendaraan Bermotor '),
('IND039', 'Ekonomi', 'Transportasi', 'Panjang Jalan '),
('IND040', 'Ekonomi', 'Transportasi', 'Rasio Kendaraan Bermotor terhadap Panjang Jalan'),
('IND041', 'Sosial', 'Pendidikan', 'Angka Melek Huruf (AMH) '),
('IND042', 'Sosial', 'Pendidikan', 'Angka Partisipasi Kasar (APK) '),
('IND043', 'Sosial', 'Pendidikan', 'Angka Partisipasi Murni (APM) '),
('IND044', 'Sosial', 'Pendidikan', 'Angka Partisipasi Sekolah (APS) '),
('IND045', 'Sosial', 'Pendidikan', 'Rata-Rata Lama Sekolah '),
('IND046', 'Sosial', 'Pendidikan', 'Angka Putus Sekolah '),
('IND047', 'Sosial', 'Pendidikan', 'Rasio Murid-Guru '),
('IND048', 'Sosial', 'Pendidikan', 'Pengeluaran Publik masuk Pendidikan sebagai Persentase dari Total Belanja Pemerintah'),
('IND049', 'Sosial', 'Kesehatan', 'Persentase Balita yang Ditolong Penolong Kelahiran '),
('IND050', 'Sosial', 'Kesehatan', 'Cakupan Imunisasi '),
('IND051', 'Sosial', 'Kesehatan', 'Persentase Balita yang Sudah Diimunisasi Lengkap '),
('IND052', 'Sosial', 'Kesehatan', 'Persentase Penduduk Sakit dengan Pengobatan sendiri '),
('IND053', 'Sosial', 'Kesehatan', 'Persentase Penduduk Sakit yang Konsultasi ke Tenaga Medis'),
('IND054', 'Sosial', 'Kesehatan', 'Persentase Penduduk Sakit yang Menjalani Rawat Inap di RS/Klinik yang Menyediakan Tenaga Medis'),
('IND055', 'Sosial', 'Fertilitas', 'Rata-Rata Jumlah Anak yang Pernah Dilahirkan/Paritas '),
('IND056', 'Sosial', 'Fertilitas', 'Anak Lahir Hidup (ALH) '),
('IND057', 'Sosial', 'Fertilitas', 'Anak Masih Hidup (AMH) '),
('IND058', 'Sosial', 'Fertilitas', 'Angka Kelahiran Kasar '),
('IND059', 'Sosial', 'Fertilitas', 'Angka Kelahiran Menurut Umur '),
('IND060', 'Sosial', 'Fertilitas', 'Angka Kelahiran Total '),
('IND061', 'Sosial', 'Fertilitas', 'Angka Kelahiran Umum '),
('IND062', 'Sosial', 'Fertilitas', 'Angka Reproduksi Neto '),
('IND063', 'Sosial', 'Fertilitas', 'Angka Reproduksi Kasar '),
('IND064', 'Sosial', 'Fertilitas', 'Rasio Anak-Ibu '),
('IND065', 'Sosial', 'Fertilitas', 'Umur Kawin Pertama (UKP) '),
('IND066', 'Sosial', 'Fertilitas', 'Angka Prevalensi Pemakaian Kontrasepsi '),
('IND067', 'Sosial', 'Fertilitas', 'Persentase Pemakai Suatu Cara KB Menurut Alat/Cara KB '),
('IND068', 'Sosial', 'Fertilitas', 'Persentase Pernah Pakai KB'),
('IND069', 'Sosial', 'Mortalitas', 'Angka Kematian Anak (AKA) '),
('IND070', 'Sosial', 'Mortalitas', 'Angka Kematian Balita (AKBa) '),
('IND071', 'Sosial', 'Mortalitas', 'Angka Kematian Bayi (AKB) '),
('IND072', 'Sosial', 'Mortalitas', 'Angka Kematian Ibu (AKI) '),
('IND073', 'Sosial', 'Mortalitas', 'Angka Kematian Kasar (AKK) '),
('IND074', 'Sosial', 'Mortalitas', 'Angka Kematian Menurut Usia (AKMU) '),
('IND075', 'Sosial', 'Mortalitas', 'Angka Kematian Neo-natal '),
('IND076', 'Sosial', 'Mortalitas', 'Angka Kematian Post Neo-natal '),
('IND077', 'Sosial', 'Mortalitas', 'Angka Harapan Hidup'),
('IND078', 'Sosial', 'Morbiditas', 'Angka Kesakitan/ Morbiditas/Persentase Penduduk yang Mempunyai Keluhan Kesehatan'),
('IND079', 'Sosial', 'Morbiditas', 'Rata-Rata Lama Sakit'),
('IND080', 'Sosial', 'Morbiditas', 'Tingkat Prevalensi '),
('IND081', 'Sosial', 'Morbiditas', 'Insidensi '),
('IND082', 'Sosial', 'Morbiditas', 'Angka Fatalitas Kasus '),
('IND083', 'Sosial', 'Morbiditas', 'Angka Daya Tular '),
('IND084', 'Sosial', 'Morbiditas', 'Tingkat Serangan '),
('IND085', 'Sosial', 'Kependudukan', 'Kepadatan Penduduk '),
('IND086', 'Sosial', 'Kependudukan', 'Laju Pertumbuhan Penduduk '),
('IND087', 'Sosial', 'Kependudukan', 'Rasio Jenis Kelamin '),
('IND088', 'Sosial', 'Kependudukan', 'Distribusi Penduduk Menurut Wilayah'),
('IND089', 'Sosial', 'Migrasi', 'Angka Migrasi Masuk '),
('IND090', 'Sosial', 'Migrasi', 'Angka Migrasi Keluar '),
('IND091', 'Sosial', 'Migrasi', 'Migrasi Neto '),
('IND092', 'Sosial', 'Migrasi', 'Migrasi Seumur Hidup '),
('IND093', 'Sosial', 'Migrasi', 'Migrasi Risen '),
('IND094', 'Sosial', 'Migrasi', 'Migrasi Total'),
('IND095', 'Sosial', 'Kemiskinan dan Ketimpangan', 'Garis Kemiskinan (GK) '),
('IND096', 'Sosial', 'Kemiskinan dan Ketimpangan', 'Persentase Penduduk Miskin '),
('IND097', 'Sosial', 'Kemiskinan dan Ketimpangan', 'Indeks Kedalaman Kemiskinan '),
('IND098', 'Sosial', 'Kemiskinan dan Ketimpangan', 'Indeks Keparahan Kemiskinan '),
('IND099', 'Sosial', 'Kemiskinan dan Ketimpangan', 'Indeks Kemiskinan Manusia (IKM) '),
('IND100', 'Sosial', 'Kemiskinan dan Ketimpangan', 'Ketimpangan Pendapatan (Ukuran Bank Dunia)'),
('IND101', 'Sosial', 'Kemiskinan dan Ketimpangan', 'Koefisien Gini'),
('IND102', 'Sosial', 'Ketenagakerjaan', 'Angkatan Kerja'),
('IND103', 'Sosial', 'Ketenagakerjaan', 'Setengah Penganggur'),
('IND104', 'Sosial', 'Ketenagakerjaan', 'Tingkat Partisipasi Angkatan Kerja (TPAK)'),
('IND105', 'Sosial', 'Ketenagakerjaan', 'Tingkat Pengangguran Terbuka (TPT)'),
('IND106', 'Sosial', 'Ketenagakerjaan', 'Tingkat Kesempatan Kerja'),
('IND107', 'Sosial', 'Ketenagakerjaan', 'Rasio Ketergantungan'),
('IND108', 'Sosial', 'Ketenagakerjaan', 'Rata-Rata Upah Harian Buruh Bangunan'),
('IND109', 'Sosial', 'Ketenagakerjaan', 'Rata-Rata Upah Harian Buruh Tani'),
('IND110', 'Sosial', 'Pembangunan Manusia', 'Indeks Pembangunan Manusia (IPM)'),
('IND111', 'Sosial', 'Pembangunan Manusia', 'Rata-Rata Pengeluaran Perkapita Riil yang Disesuaikan (Daya Beli)'),
('IND112', 'Sosial', 'Pembangunan Manusia', 'Indeks Pembangunan Gender (IPG) '),
('IND113', 'Sosial', 'Pembangunan Manusia', 'Indeks Pemberdayaan Gender (IDG) '),
('IND114', 'Lainnya', 'Lainnya', 'Lainnya');

-- --------------------------------------------------------

--
-- Table structure for table `indikator_sum`
--

CREATE TABLE `indikator_sum` (
  `jumlah` int(11) NOT NULL,
  `id_indikator` varchar(6) NOT NULL,
  `sub_indikator` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `katakunci_indikator`
--

CREATE TABLE `katakunci_indikator` (
  `id_indikator` varchar(6) NOT NULL,
  `katakunci` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `katakunci_indikator`
--

INSERT INTO `katakunci_indikator` (`id_indikator`, `katakunci`) VALUES
('IND001', 'ekspor OR impor OR neraca perdagangan'),
('IND002', 'Indeks Harga Perdagangan Besar (IHPB) OR indeks harga perdagangan besar OR IHPB'),
('IND003', 'Indeks Harga Konsumen (IHK) OR indeks harga konsumen OR IHK'),
('IND004', 'inflasi OR deflasi OR laju inflasi OR inflasi bulanan OR inflasi tahunan OR inflasi tahun kalender OR inflasi inti OR inflasi volatile food OR inflasi administered prices'),
('IND005', 'Indeks Konsumsi Rumah Tangga (IKRT) OR indeks konsumsi rumah tangga OR IKRT'),
('IND006', 'inflasi perdesaan OR deflasi perdesaan'),
('IND007', 'Indeks Tendensi Bisnis (ITB) OR indeks tendensi bisnis OR ITB OR tendensi bisnis'),
('IND008', 'Indeks Indikator Kini (IIK) OR indeks indikator kini OR IIK'),
('IND009', 'Indeks Indikator Mendatang (IIM) OR indeks indikator mendatang OR IIM'),
('IND010', 'Indeks Tendensi Konsumen (ITK) OR indeks tendensi konsumen OR ITK OR tendensi konsumen'),
('IND011', 'Indeks Indikator Kini (IIK) OR indeks indikator kini OR IIK'),
('IND012', 'Indeks Indikator Mendatang (IIM) OR indeks indikator mendatang OR IIM'),
('IND013', 'Nilai Tukar Petani (NTP) OR nilai tukar petani OR NTP OR Nilai Tukar Usaha Rumah Tangga Pertanian (NTUP) OR nilai tukar usaha rumah tangga pertanian OR NTUP'),
('IND014', 'Indeks Harga yang Diterima Petani (It) OR indeks harga yang diterima petani OR It'),
('IND015', 'Indeks Harga yang Dibayar Petani (Ib) OR indeks harga yang dibayar petani OR Ib'),
('IND016', 'rata-rata harga gabah OR harga gabah OR Rata-rata Harga Gabah Kering Giling (GKG) OR harga gabah kering giling OR harga GKG OR Rata-rata Harga Gabah Kering Panen (GKP) OR harga gabah kering panen OR harga GKP OR Rata-rata Harga Gabah Kualitas Rendah (GKR) OR harga gabah kualitas rendah OR harga GKR'),
('IND017', 'Rata-Rata Lama Menginap Tamu (Asing dan Dalam Negeri) OR rata-rata lama menginap tamu asing OR rata-rata lama menginap tamu Indonesia OR rata-rata lama menginap tamu'),
('IND018', 'rata-rata lama tinggal wisatawan mancanegara OR rata-rata lama tinggal wisman OR rata-rata lama tinggal wisatawan'),
('IND019', 'rata-rata pengeluaran per wisman per hari per kunjungan'),
('IND020', 'Tingkat Penghunian Kamar (TPK) OR tingkat penghunian kamar OR TPK'),
('IND021', 'penerimaan dari wisatawan mancanegara OR penerimaan dari wisman OR jumlah kunjungan wisatawan mancanegara OR jumlah kunjungan wisman OR kunjungan wisatawan mancanegara OR kunjungan wisman OR jumlah wisatawan mancanegara OR jumlah wisman '),
('IND022', 'Produk Domestik Bruto (PDB) OR Produk Domestik Regional Bruto (PDRB) OR produk domestik bruto OR produk domestik regional bruto OR PDB OR PDRB OR PDB atas dasar harga berlaku OR PDB atas dasar harga konstan OR PDB ADHB OR PDB ADHK OR PDRB atas dasar harga berlaku OR PDRB atas dasar harga konstan OR PDRB ADHB OR PDRB ADHK'),
('IND023', 'laju pertumbuhan PDB OR laju pertumbuhan PDRB OR pertumbuhan ekonomi OR laju pertumbuhan ekonomi'),
('IND024', 'indeks implisit'),
('IND025', 'distribusi persentase PDB OR distribusi persentase PDRB OR distribusi PDB OR distribusi PDRB'),
('IND026', 'PDB per kapita OR PDRB per kapita'),
('IND027', 'rasio modal-output marginal OR ICOR'),
('IND028', 'rasio tenaga kerja-output marginal OR ILOR'),
('IND029', 'pertumbuhan produksi industri pengolahan OR pertumbuhan produksi industri OR PPI OR Industri Kecil Menengah (IKM) OR industri kecil menengah OR IKM OR Industri Besar Sedang (IBS) OR industri besar sedang OR IBS'),
('IND030', 'indeks produksi industri pengolahan'),
('IND031', 'rasio penumpang per pesawat udara OR RPPU OR penumpang per pesawat OR jumlah penumpang angkutan udara OR pengguna angkutan udara OR jumlah pengguna angkutan udara'),
('IND032', 'rasio barang per pesawat udara OR RBPU OR jumlah barang yang diangkut OR rasio jumlah barang per pesawat'),
('IND033', 'rasio penumpang per kapal OR RPK OR jumlah penumpang angkutan laut OR penumpang angkutan laut'),
('IND034', 'rasio barang per kapal OR RBK. jumlah barang yang dibongkar OR jumlah barang yang dimuat OR jumlah barang yang diangkut naik OR jumlah barang yang diangkut turun'),
('IND035', 'rasio penduduk terhadap mobil penumpang OR RPMP'),
('IND036', 'rasio penduduk terhadap kendaraan bermotor OR RPKB'),
('IND037', 'rasio penduduk terhadap bus umum OR RPBU'),
('IND038', 'jumlah kendaraan bermotor'),
('IND039', 'panjang jalan'),
('IND040', 'rasio kendaraan bermotor terhadap panjang jalan OR RKBPJ'),
('IND041', 'Angka Melek Huruf (AMH) OR angka melek huruf OR AMH'),
('IND042', 'Angka Partisipasi Kasar (APK) OR angka partisipasi kasar OR APK'),
('IND043', 'Angka Partisipasi Murni (APM) OR angka partisipasi murni OR APM'),
('IND044', 'Angka Partisipasi Sekolah (APS) OR angka partisipasi sekolah OR APS'),
('IND045', 'rata-rata lama sekolah OR tingkat pendidikan'),
('IND046', 'angka putus sekolah'),
('IND047', 'rasio murid-guru'),
('IND048', 'pengeluaran publik masuk pendidikan sebagai persentase dari total belanja pemerintah'),
('IND049', 'persentase balita yang ditolong penolong kelahiran OR persentase bayi lahir ditolong nakes OR persentase bayi lahir ditolong non-nakes'),
('IND050', 'cakupan imunisasi'),
('IND051', 'persentase balita yang sudah diimunisasi lengkap'),
('IND052', 'persentase penduduk sakit dengan pengobatan sendiri'),
('IND053', 'persentase penduduk sakit yang konsultasi ke tenaga medis'),
('IND054', 'persentase penduduk sakit yang menjalani rawat inap di RS/klinik yang menyediakan tenaga medis OR persentase penduduk sakit yang menjalani rawat inap di rumah sakit yang menyediakan tenaga medis OR persentase penduduk sakit yang menjalani rawat inap di RS yang menyediakan tenaga medis OR persentase penduduk sakit yang menjalani rawat inap di klinik yang menyediakan tenaga medis'),
('IND055', 'rata-rata jumlah anak yang pernah dilahirkan/paritas'),
('IND056', 'Anak Lahir Hidup (ALH) OR anak lahir hidup OR ALH'),
('IND057', 'Anak Masih Hidup (AMH) OR anak masih hidup OR AMH'),
('IND058', 'angka kelahiran kasar OR CBR'),
('IND059', 'angka kelahiran menurut umur OR ASFR'),
('IND060', 'angka kelahiran total OR TFR'),
('IND061', 'angka kelahiran umum OR GFR'),
('IND062', 'angka reproduksi neto OR NRR'),
('IND063', 'angka reproduksi kasar OR GRR'),
('IND064', 'rasio anak-ibu'),
('IND065', 'Umur Kawin Pertama (UKP) OR umur kawin pertama OR UKP'),
('IND066', 'angka prevalensi pemakaian kontrasepsi'),
('IND067', ' persentase pemakai suatu cara KB menurut alat/cara KB OR PUS memakai alat/cara KB'),
('IND068', 'persentase pernah pakai KB OR persentase PUS yang pernah memakai suatu cara KB'),
('IND069', 'Angka Kematian Anak (AKA) OR angka kematian anak OR AKA'),
('IND070', 'Angka Kematian Balita (AKBa) OR angka kematian balita OR AKBa'),
('IND071', 'Angka Kematian Bayi (AKB) OR angka kematian bayi OR AKB'),
('IND072', 'Angka Kematian Ibu (AKI) OR angka kematian ibu OR AKI'),
('IND073', 'Angka Kematian Kasar (AKK) OR angka kematian kasar OR AKK'),
('IND074', 'Angka Kematian Menurut Usia (AKMU) OR angka kematian menurut usia OR AKMU'),
('IND075', 'angka kematian neo-natal OR AKNeo'),
('IND076', 'angka kematian post neo-natal OR AKPNeo'),
('IND077', 'Angka Harapan Hidup (AHH) OR angka harapan hidup OR AHH OR harapan hidup'),
('IND078', 'angka kesakitan OR angka morbiditas OR morbiditas OR persentase penduduk yang mempunyai keluhan kesehatan'),
('IND079', 'rata-rata lama sakit'),
('IND080', 'tingkat prevalensi'),
('IND081', 'insidensi'),
('IND082', 'angka fatalitas kasus'),
('IND083', 'angka daya tular'),
('IND084', 'tingkat serangan'),
('IND085', 'kepadatan penduduk OR jumlah penduduk OR jumlah populasi penduduk'),
('IND086', 'laju pertumbuhan penduduk OR pertumbuhan penduduk'),
('IND087', 'rasio jenis kelamin OR sex ratio OR SR'),
('IND088', 'distribusi penduduk menurut wilayah OR persentase penduduk menurut wilayah'),
('IND089', 'angka migrasi masuk OR migrasi masuk'),
('IND090', 'angka migrasi keluar OR migrasi keluar'),
('IND091', 'angka migrasi neto OR migrasi neto'),
('IND092', 'migrasi seumur hidup OR migrasi semasa hidup'),
('IND093', 'angka migrasi risen OR migrasi risen'),
('IND094', 'angka migrasi total OR migrasi total'),
('IND095', 'Garis Kemiskinan (GK) OR garis kemiskinan OR garis kemiskinan makanan OR garis kemiskinan bukan makanan OR garis kemiskinan nonmakanan OR GK OR GKM OR GKBM OR GKNM OR kemiskinan OR angka kemiskinan'),
('IND096', 'persentase penduduk miskin OR persentase kemiskinan OR jumlah penduduk miskin OR tingkat kemiskinan OR jumlah masyarakat miskin'),
('IND097', 'indeks kedalaman kemiskinan OR kedalaman kemiskinan'),
('IND098', 'indeks keparahan kemiskinan OR keparahan kemiskinan'),
('IND099', 'Indeks Kemiskinan Manusia (IKM) OR indeks kemiskinan manusia OR IKM'),
('IND100', 'ketimpangan pendapatan (ukuran bank dunia) OR ketimpangan bank dunia'),
('IND101', 'koefisien gini OR gini ratio OR rasio gini OR tingkat ketimpangan pendapatan OR ketimpangan pendapatan OR ketimpangan'),
('IND102', 'angkatan kerja OR pengangguran OR penganggur OR penduduk usia kerja OR jumlah penduduk yang bekerja OR jumlah penduduk bekerja OR jumlah pengangguran OR jumlah angkatan kerja OR jumlah penduduk angkatan kerja OR jumlah penduduk bukan angkatan kerja'),
('IND103', 'angka setengah pengangguran OR setengah penganggur OR setengah pengangguran OR pekerja setengah penganggur'),
('IND104', 'Tingkat Partisipasi Angkatan Kerja (TPAK) OR tingkat partisipasi angkatan kerja OR TPAK'),
('IND105', 'Tingkat Pengangguran Terbuka (TPT) OR tingkat pengangguran terbuka OR TPT OR tingkat pengangguran'),
('IND106', 'tingkat kesempatan kerja OR kesempatan kerja'),
('IND107', 'rasio ketergantungan'),
('IND108', 'rata-rata upah harian buruh bangunan OR upah nomial harian buruh bangunan'),
('IND109', 'rata-rata upah harian buruh tani OR upah nominal harian buruh tani'),
('IND110', 'Indeks Pembangunan Manusia (IPM) OR indeks pembangunan manusia OR IPM'),
('IND111', 'rata-rata pengeluaran perkapita riil yang disesuaikan (daya beli) OR daya beli masyarakat'),
('IND112', 'Indeks Pembangunan Gender (IPG) OR indeks pembangunan gender OR IPG'),
('IND113', 'Indeks Pemberdayaan Gender (IDG) OR indeks pemberdayaan gender OR IDG'),
('IND114', 'Potensi Desa (Podes) OR Podes OR ');

-- --------------------------------------------------------

--
-- Table structure for table `ner_output`
--

CREATE TABLE `ner_output` (
  `id_berita` int(11) NOT NULL,
  `indikator` text NOT NULL,
  `tokoh` text NOT NULL,
  `posisi` text NOT NULL,
  `organisasi` text NOT NULL,
  `lokasi` text NOT NULL,
  `kutipan` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sentimen`
--

CREATE TABLE `sentimen` (
  `id_berita` int(11) NOT NULL,
  `id_indikator` varchar(6) NOT NULL,
  `indikator` varchar(32) NOT NULL,
  `sentimen` varchar(10) NOT NULL,
  `jenis` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sum_ner`
--

CREATE TABLE `sum_ner` (
  `entitas` varchar(50) NOT NULL,
  `indikator` varchar(32) NOT NULL,
  `jenis_entitas` varchar(24) NOT NULL,
  `jumlah` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sum_tag`
--

CREATE TABLE `sum_tag` (
  `waktu` date NOT NULL,
  `tag` varchar(50) NOT NULL,
  `jumlah` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sum_tweets`
--

CREATE TABLE `sum_tweets` (
  `tanggal` date NOT NULL,
  `kategori` varchar(35) NOT NULL,
  `provinsi` varchar(30) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `jenis` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tweets`
--

CREATE TABLE `tweets` (
  `kategori` tinytext NOT NULL,
  `status_posted` datetime NOT NULL,
  `user_desc` longtext CHARACTER SET utf8mb4,
  `user_status_count` int(11) NOT NULL,
  `user_name` varchar(25) NOT NULL,
  `user_target_reply` varchar(25) DEFAULT NULL,
  `user_verified` varchar(6) NOT NULL,
  `status_text` text CHARACTER SET utf8mb4 NOT NULL,
  `status_hashtags` text CHARACTER SET utf8mb4,
  `user_location` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  `user_following` int(11) NOT NULL,
  `user_followers` int(11) NOT NULL,
  `retweets` int(11) NOT NULL,
  `coordinate` text,
  `country_code` varchar(3) DEFAULT NULL,
  `provinsi` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `beritasum_indikator`
--
ALTER TABLE `beritasum_indikator`
  ADD PRIMARY KEY (`waktu`,`indikator`);

--
-- Indexes for table `beritasum_sumber`
--
ALTER TABLE `beritasum_sumber`
  ADD PRIMARY KEY (`waktu`,`sumber`);

--
-- Indexes for table `berita_detail`
--
ALTER TABLE `berita_detail`
  ADD PRIMARY KEY (`id_berita`),
  ADD UNIQUE KEY `id_berita` (`id_berita`),
  ADD UNIQUE KEY `judul` (`judul`,`waktu`,`sumber`);

--
-- Indexes for table `indikator_ref`
--
ALTER TABLE `indikator_ref`
  ADD PRIMARY KEY (`id_indikator`);

--
-- Indexes for table `indikator_sum`
--
ALTER TABLE `indikator_sum`
  ADD PRIMARY KEY (`id_indikator`);

--
-- Indexes for table `katakunci_indikator`
--
ALTER TABLE `katakunci_indikator`
  ADD PRIMARY KEY (`id_indikator`);

--
-- Indexes for table `ner_output`
--
ALTER TABLE `ner_output`
  ADD PRIMARY KEY (`id_berita`),
  ADD KEY `id_berita` (`id_berita`) USING BTREE;

--
-- Indexes for table `sentimen`
--
ALTER TABLE `sentimen`
  ADD UNIQUE KEY `sentimen_berita` (`id_berita`,`jenis`);

--
-- Indexes for table `sum_ner`
--
ALTER TABLE `sum_ner`
  ADD UNIQUE KEY `entitas` (`entitas`,`indikator`,`jenis_entitas`);

--
-- Indexes for table `sum_tweets`
--
ALTER TABLE `sum_tweets`
  ADD PRIMARY KEY (`tanggal`,`kategori`,`provinsi`);

--
-- Indexes for table `tweets`
--
ALTER TABLE `tweets`
  ADD PRIMARY KEY (`status_posted`,`user_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `berita_detail`
--
ALTER TABLE `berita_detail`
  MODIFY `id_berita` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ner_output`
--
ALTER TABLE `ner_output`
  MODIFY `id_berita` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sentimen`
--
ALTER TABLE `sentimen`
  MODIFY `id_berita` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
