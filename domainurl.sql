/*
 Navicat Premium Data Transfer

 Source Server         : domain
 Source Server Type    : MySQL
 Source Server Version : 80013
 Source Host           : localhost:3306
 Source Schema         : domain2

 Target Server Type    : MySQL
 Target Server Version : 80013
 File Encoding         : 65001

 Date: 22/09/2019 14:01:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, '会员管理', 1);
INSERT INTO `menu` VALUES (2, '订单管理', 2);
INSERT INTO `menu` VALUES (3, '分类管理', 3);
INSERT INTO `menu` VALUES (4, '城市联动', 4);
INSERT INTO `menu` VALUES (5, '管理员管理', 5);

-- ----------------------------
-- Table structure for newuser
-- ----------------------------
DROP TABLE IF EXISTS `newuser`;
CREATE TABLE `newuser`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of newuser
-- ----------------------------
INSERT INTO `newuser` VALUES (1, 'pbkdf2_sha256$150000$nyCNeDZtDk3k$fLNoIVsPuIcR2qxep2qQNPgE+sxt4LLJIcEy54dL3Tk=', '2019-09-22 05:27:39.149000', 0, 'admin', '', '', '', 0, 1, '2019-09-12 06:53:52.084000');
INSERT INTO `newuser` VALUES (8, 'pbkdf2_sha256$150000$jmpTyjDRg0zh$Nue2W17IlDRIZBBlyxkKSkjYBwz5f55y2igP1g6TO0Q=', '2019-09-12 09:25:44.368000', 0, 'admin2', '', '', '', 0, 1, '2019-09-12 09:20:47.604000');
INSERT INTO `newuser` VALUES (10, 'pbkdf2_sha256$150000$Parx9WHvMkwz$KHh0HhaeKGi8I/C6+Z8GA9EmzaoAABVYuuV29yDs0hY=', NULL, 0, 'admin3', '', '', '', 0, 1, '2019-09-22 05:31:16.162000');

-- ----------------------------
-- Table structure for newuser_groups
-- ----------------------------
DROP TABLE IF EXISTS `newuser_groups`;
CREATE TABLE `newuser_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `newuser_groups_newuser_id_group_id_6e81469f_uniq`(`newuser_id`, `group_id`) USING BTREE,
  INDEX `newuser_groups_group_id_835ce3cd_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `newuser_groups_group_id_835ce3cd_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `newuser_groups_newuser_id_b04390cd_fk_newuser_id` FOREIGN KEY (`newuser_id`) REFERENCES `newuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for newuser_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `newuser_user_permissions`;
CREATE TABLE `newuser_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `newuser_user_permissions_newuser_id_permission_id_88f8765a_uniq`(`newuser_id`, `permission_id`) USING BTREE,
  INDEX `newuser_user_permiss_permission_id_aadb73e4_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `newuser_user_permiss_permission_id_aadb73e4_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `newuser_user_permissions_newuser_id_1b5c9cdf_fk_newuser_id` FOREIGN KEY (`newuser_id`) REFERENCES `newuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nameurl` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `namemethod` varchar(56) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `relationself_id` int(11) DEFAULT NULL,
  `relationship_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `permission_relationself_id_0584d9f3_fk_permission_id`(`relationself_id`) USING BTREE,
  INDEX `permission_relationship_id_47ef78db_fk_menu_id`(`relationship_id`) USING BTREE,
  CONSTRAINT `permission_relationself_id_0584d9f3_fk_permission_id` FOREIGN KEY (`relationself_id`) REFERENCES `permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `permission_relationship_id_47ef78db_fk_menu_id` FOREIGN KEY (`relationship_id`) REFERENCES `menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of permission
-- ----------------------------
INSERT INTO `permission` VALUES (26, '管理员列表', '/adminuser/', 'GET', NULL, 5);
INSERT INTO `permission` VALUES (27, '角色管理', '/adminrole/', 'GET', NULL, 5);
INSERT INTO `permission` VALUES (28, '菜单分类', '/adminmenu/', 'GET', NULL, 5);
INSERT INTO `permission` VALUES (29, '权限管理', '/adminpermission/', 'GET', NULL, 5);
INSERT INTO `permission` VALUES (34, '管理员列表添加', '/adminuserdata/', 'POST', 26, NULL);
INSERT INTO `permission` VALUES (35, '管理员列表编辑', '/adminuserdata/', 'POST', 26, NULL);
INSERT INTO `permission` VALUES (36, '管理员列表删除', '/adminuserdata/', 'DELETE', 26, NULL);
INSERT INTO `permission` VALUES (37, '管理员列表表格渲染', '/adminuserdata/', 'GET', 26, NULL);
INSERT INTO `permission` VALUES (38, '角色管理添加', '/adminroledata/', 'POST', 27, NULL);
INSERT INTO `permission` VALUES (39, '角色管理编辑', '/adminroleiframe/', 'GET', 27, NULL);
INSERT INTO `permission` VALUES (40, '角色管理编辑渲染', '/adminroleset/', 'GET', 27, NULL);
INSERT INTO `permission` VALUES (41, '角色管理编辑确认', '/adminroleedit/', 'POST', 27, NULL);
INSERT INTO `permission` VALUES (42, '角色管理删除', '/adminroledata/', 'DELETE', 27, NULL);
INSERT INTO `permission` VALUES (43, '角色管理表格渲染', '/adminroledata/', 'GET', 27, NULL);
INSERT INTO `permission` VALUES (44, '菜单分类添加', '/adminmenudata/', 'POST', 28, NULL);
INSERT INTO `permission` VALUES (45, '菜单分类表格渲染', '/adminmenudata/', 'GET', 28, NULL);
INSERT INTO `permission` VALUES (46, '菜单分类删除', '/adminmenudata/', 'DELETE', 28, NULL);
INSERT INTO `permission` VALUES (47, '权限管理添加', '/adminpermissiondata/', 'POST', 29, NULL);
INSERT INTO `permission` VALUES (48, '权限管理表格渲染', '/adminpermissiondata/', 'GET', 29, NULL);
INSERT INTO `permission` VALUES (49, '权限管理删除', '/adminpermissiondata/', 'DELETE', 29, NULL);
INSERT INTO `permission` VALUES (50, '权限管理编辑', '/adminpermissionedit/', 'GET', 29, NULL);
INSERT INTO `permission` VALUES (51, '权限管理编辑更新', '/adminpermissiondata/', 'PUT', 29, NULL);

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, '超级管理员');
INSERT INTO `role` VALUES (2, '客服');

-- ----------------------------
-- Table structure for role_relationpermiss
-- ----------------------------
DROP TABLE IF EXISTS `role_relationpermiss`;
CREATE TABLE `role_relationpermiss`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `role_relationpermiss_role_id_permission_id_4275d2af_uniq`(`role_id`, `permission_id`) USING BTREE,
  INDEX `role_relationpermiss_permission_id_13bd561c_fk_permission_id`(`permission_id`) USING BTREE,
  CONSTRAINT `role_relationpermiss_permission_id_13bd561c_fk_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `role_relationpermiss_role_id_e769d578_fk_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 79 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_relationpermiss
-- ----------------------------
INSERT INTO `role_relationpermiss` VALUES (150, 1, 26);
INSERT INTO `role_relationpermiss` VALUES (151, 1, 27);
INSERT INTO `role_relationpermiss` VALUES (152, 1, 28);
INSERT INTO `role_relationpermiss` VALUES (153, 1, 29);
INSERT INTO `role_relationpermiss` VALUES (154, 1, 34);
INSERT INTO `role_relationpermiss` VALUES (155, 1, 35);
INSERT INTO `role_relationpermiss` VALUES (156, 1, 36);
INSERT INTO `role_relationpermiss` VALUES (157, 1, 37);
INSERT INTO `role_relationpermiss` VALUES (158, 1, 38);
INSERT INTO `role_relationpermiss` VALUES (159, 1, 39);
INSERT INTO `role_relationpermiss` VALUES (160, 1, 40);
INSERT INTO `role_relationpermiss` VALUES (161, 1, 41);
INSERT INTO `role_relationpermiss` VALUES (162, 1, 42);
INSERT INTO `role_relationpermiss` VALUES (163, 1, 43);
INSERT INTO `role_relationpermiss` VALUES (164, 1, 44);
INSERT INTO `role_relationpermiss` VALUES (165, 1, 45);
INSERT INTO `role_relationpermiss` VALUES (166, 1, 46);
INSERT INTO `role_relationpermiss` VALUES (167, 1, 47);
INSERT INTO `role_relationpermiss` VALUES (168, 1, 48);
INSERT INTO `role_relationpermiss` VALUES (169, 1, 49);
INSERT INTO `role_relationpermiss` VALUES (170, 1, 50);
INSERT INTO `role_relationpermiss` VALUES (171, 1, 51);

-- ----------------------------
-- Table structure for role_relationship
-- ----------------------------
DROP TABLE IF EXISTS `role_relationship`;
CREATE TABLE `role_relationship`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `newuser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `role_relationship_role_id_newuser_id_2ad6f75c_uniq`(`role_id`, `newuser_id`) USING BTREE,
  INDEX `role_relationship_newuser_id_6aa9452c_fk_newuser_id`(`newuser_id`) USING BTREE,
  CONSTRAINT `role_relationship_newuser_id_6aa9452c_fk_newuser_id` FOREIGN KEY (`newuser_id`) REFERENCES `newuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `role_relationship_role_id_a2271437_fk_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_relationship
-- ----------------------------
INSERT INTO `role_relationship` VALUES (2, 1, 1);
INSERT INTO `role_relationship` VALUES (5, 2, 8);
INSERT INTO `role_relationship` VALUES (7, 2, 10);

SET FOREIGN_KEY_CHECKS = 1;
