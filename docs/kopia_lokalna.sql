--
-- PostgreSQL database dump
--

\restrict fcfyriaEfvT6IWewQYVEQCShkH87nCcvpVgbB7FaAaVqvy4izFzpKijtBfkC0nC

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-07-12 18:42:37

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5127 (class 1262 OID 311296)
-- Name: project_job; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE project_job WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Polish_Poland.1250';


ALTER DATABASE project_job OWNER TO postgres;

\unrestrict fcfyriaEfvT6IWewQYVEQCShkH87nCcvpVgbB7FaAaVqvy4izFzpKijtBfkC0nC
\connect project_job
\restrict fcfyriaEfvT6IWewQYVEQCShkH87nCcvpVgbB7FaAaVqvy4izFzpKijtBfkC0nC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5099 (class 0 OID 336465)
-- Dependencies: 220
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version (version_num) VALUES ('ed1e0bf5bedd');


--
-- TOC entry 5100 (class 0 OID 336482)
-- Dependencies: 221
-- Data for Name: calendar_work_condition_changes; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5101 (class 0 OID 336494)
-- Dependencies: 222
-- Data for Name: calendar_work_days; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5102 (class 0 OID 336509)
-- Dependencies: 223
-- Data for Name: keyscalculatorpatryk; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.keyscalculatorpatryk (id, income_tax, vat, inpost_parcel_locker, inpost_courier, inpost_cash_of_delivery_courier, dpd, allegro_matt, without_smart) VALUES ('2dd1daa8-2b7a-4cc5-8e57-e91429b8fae2', 0.19, 0.23, 11.49, 14.99, 20, 20, 9.99, 20);


--
-- TOC entry 5103 (class 0 OID 336515)
-- Dependencies: 224
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.logs (id, username, description, date) VALUES ('7952f957-b4d2-4e29-955e-d82d7e08e90d', 'ChaLLengeR', 'auth:login', '2026-07-11 12:47:22.899002+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3295b618-c909-4e25-9ff2-10cb01bfd0e0', 'ChaLLengeR', 'tasks:collection', '2026-07-11 12:47:25.619668+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b9d9396b-4b95-4178-b142-e117d751c9bd', 'ChaLLengeR', 'tasks:statistics', '2026-07-11 12:47:25.668998+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d8a36383-2e78-412b-95c9-8db638f32d34', 'ChaLLengeR', 'tasks:collection', '2026-07-11 12:55:26.648437+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('db642322-aacd-41b6-86b8-672eaf878b6b', 'ChaLLengeR', 'tasks:statistics', '2026-07-11 12:55:26.703358+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a5199753-6e01-42f5-b750-ec4a90a15b01', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 12:55:26.790756+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3a33ac75-4214-4f37-ba3a-399ce942fb7c', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 12:55:40.528658+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ce6a1a6f-00fe-4943-b8f1-34c3ab52591b', 'ChaLLengeR', 'tasks:collection', '2026-07-11 12:55:40.532729+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('106f320b-741f-4946-9391-66733489a22d', 'ChaLLengeR', 'tasks:statistics', '2026-07-11 12:55:40.567724+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5bd1d340-d74e-46aa-94a7-3a3f9a2f890d', 'ChaLLengeR', 'outstanding_money:collection', '2026-07-11 12:55:55.122612+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('71c91333-a3a8-415a-a659-764aa8c0866f', 'ChaLLengeR', 'outstanding_money:create_list', '2026-07-11 12:56:05.363172+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7199118a-99c3-4171-a9f2-830084eb94cb', 'ChaLLengeR', 'outstanding_money:collection', '2026-07-11 12:56:05.380294+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('21b17785-2867-4ac5-82bd-52c95d60ca3b', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:27:38.404268+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('69253103-77ad-4a8d-9162-e8eb56acb775', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:27:43.218319+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f364fb52-2036-4e3e-8d8e-e1d02559f91e', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:27:48.03163+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('61d5d51a-8f0e-41b4-948c-1b9b8056a65f', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:27:53.100385+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f7307dd3-27df-4348-a06d-030697f2393e', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:27:58.471683+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('53a54a63-9553-4e65-92af-d0fba8c94b32', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:28:03.482359+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('da329af3-85ae-497d-8f5d-7e594afe0f41', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:29:02.384295+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7802b9ad-ea4f-44fe-9988-2511005b09ce', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:29:34.797637+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e6bcd87b-73ff-49b3-a18b-33c6cd794838', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:29:39.811251+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('33eaaf72-3602-445e-a6dc-b8c3589a331c', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:29:55.26761+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('03bec221-1913-429d-8add-2ff9fd5ac53c', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:34:19.898987+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('57d5bc71-463a-4015-9613-6315e8334421', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:43:29.909166+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fe32352b-2a2e-46aa-874c-2940717b0742', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:43:30.110685+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('159519ed-9928-4c76-94b0-63b5c6294249', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 13:43:30.128125+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a56d9ea0-af37-4f8a-8719-aea2e43ddc49', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:43:30.18072+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bf9cd82e-e299-4da5-84bf-922413678a0d', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 13:43:30.280786+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d80fbc4a-0536-4c94-8fdc-06f44b0bc00a', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 13:43:30.28342+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b287e9a0-ea28-4e8c-8f8d-fee3f9537cee', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:43:30.30351+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d1bcf358-e6f0-4433-b77c-8facc4bf1b61', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:43:30.315372+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e9800f3e-4ff0-45f2-81a2-be66a2837d00', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:43:30.321001+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2776f771-8c51-4984-ad49-d43c0c34ece8', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 13:43:30.319284+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('181ff8e1-5127-4be1-aca0-dd9992931865', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 13:43:30.335101+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ae4eecf4-1d3e-4995-9420-845994b7f939', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:43:30.343938+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b38055a7-66f8-42f2-8417-2dd59ab84c2d', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:43:50.824556+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('216150bb-ceca-452b-8ee9-b72c7d141825', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 13:44:40.128981+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('722362d5-7c0a-47a7-8fec-b9fb2ed79705', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:44:40.369865+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1cad49d8-c44e-4310-8e7c-f67a5c1bac7b', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 13:44:40.377382+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('842804e6-a8d1-4bb1-967c-555d1bd797f4', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 13:44:40.37705+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('46309778-564c-4b96-a7e0-f5b724a59c87', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 13:44:40.379682+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('be278ad7-bfe1-47b5-aceb-6d7e0426adb9', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:44:40.402042+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('80a63c2b-3490-42b0-930d-5c82132b8df5', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:44:40.413858+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2a7ddd1b-c2e5-43c7-aa83-6ee3f9f31d71', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 13:44:40.416846+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6f813c61-8386-4284-ac9a-526934515ecc', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:44:40.417145+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('78f9cee7-7f28-44f2-ab11-7f36746ba7ad', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 13:44:40.516814+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9a12c9f6-730d-4b9f-9941-34e35096bc82', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:44:40.532972+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5488bf3d-8463-4a49-b8ea-83a74a9790a2', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:44:40.546134+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d9945ba3-e86f-4169-a58b-8c88da57186b', 'ChaLLengeR', 'rental:create_apartment', '2026-07-11 13:45:31.686315+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('db853e51-3699-4eff-8227-5c914bbe1066', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:45:31.700867+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ecf59a60-1739-42bd-af63-5d6cb8a9cb95', 'ChaLLengeR', 'rental:create_apartment', '2026-07-11 13:46:02.306159+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('413823b9-6f1f-41d0-b61f-c84e70180451', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:46:02.316456+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e7388985-a9df-4fac-a6d7-ce00a3a80a77', 'ChaLLengeR', 'rental:create_apartment', '2026-07-11 13:46:10.847409+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('47fe8822-6d95-4691-877a-a60fb9ab5801', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:46:10.862695+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('81973213-350a-4e33-8e27-7d52cccb547b', 'ChaLLengeR', 'rental:create_apartment', '2026-07-11 13:46:18.845477+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('628d5084-149c-4ff7-8399-92e18e9efe1d', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 13:46:18.860217+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('84add050-f38a-4b10-9983-53f1cb956dd7', 'ChaLLengeR', 'rental:create_tenant', '2026-07-11 13:46:40.646687+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b4efb623-8f32-47c0-8ae9-94866f1d3b87', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:46:40.657504+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('64662b5c-67f4-4854-9484-569a56d45d20', 'ChaLLengeR', 'rental:create_tenant', '2026-07-11 13:46:48.794863+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('01dad7c7-08b6-4c2f-9e05-ff76afeac10e', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:46:48.810702+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('491320ed-e980-460c-98f4-ea66b83503f5', 'ChaLLengeR', 'rental:create_tenant', '2026-07-11 13:46:58.279469+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c20ccd20-40bc-4388-aba9-f32509d96b44', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:46:58.295595+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cba4a908-f872-471b-aa60-fb889fd546e0', 'ChaLLengeR', 'rental:create_tenant', '2026-07-11 13:47:03.883535+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bc442213-eed2-4611-8b49-72309cec6b6f', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 13:47:03.894045+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f947872b-6d8e-432b-a64b-f007f735d980', 'ChaLLengeR', 'rental:create_tenancy', '2026-07-11 13:51:14.484116+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('078970a1-2f0e-4ad1-9240-f9f6c3573f65', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 13:51:14.505403+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2e432b76-e3d8-41b6-af96-ca898ebdc485', 'ChaLLengeR', 'rental:create_tenancy', '2026-07-11 13:51:34.875441+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('33813390-3b06-4234-82c3-79b5b9fe5acd', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 13:51:34.887063+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b4f2bc4f-0a72-4b29-81ff-f8ad902dc892', 'ChaLLengeR', 'rental:create_tenancy', '2026-07-11 13:51:52.509844+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('52b40009-aa90-4454-aebd-e3ece1a47dc0', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 13:51:52.519772+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8e8a9d0b-c55f-4169-9f29-d87912b0e015', 'ChaLLengeR', 'rental:create_cost_type', '2026-07-11 13:53:14.894111+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4316572c-b9ea-46b3-8d6f-ac05767aa221', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 13:53:14.90538+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('47b4ef2c-2fad-40e3-a1de-9a6feb848de8', 'ChaLLengeR', 'rental:create_cost_type', '2026-07-11 13:53:22.775805+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1f9351d1-e674-4b00-b5bb-78d89530e1c6', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 13:53:22.785367+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a86a2c27-7d12-4ddf-b3a9-b7304bf74b25', 'ChaLLengeR', 'rental:create_cost_type', '2026-07-11 13:53:29.81946+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('81243a7d-72d4-4b56-b157-0382e0213c8b', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 13:53:29.832753+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fc2e2103-305b-43d0-a74d-d1771c8fdbd0', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 13:57:03.431136+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c4d38617-abb4-47db-a655-970c3b9abfc5', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 13:57:03.444754+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('83c96c36-c8c3-4bb6-8023-01b0c94950f4', 'ChaLLengeR', 'rental:update_apartment_cost', '2026-07-11 13:59:30.553249+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('096a6dd4-2feb-4fdd-bb23-ebfd6db2639f', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 13:59:30.574263+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5d53b6d3-ff50-4c2e-a4e3-be1542a6d67f', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 13:59:46.879754+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7937ca8c-bac6-4ca3-a30b-98141f39482d', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 13:59:46.889645+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ed321ecc-3275-4d56-8f3a-4d1572aac7b1', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 14:00:05.765057+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5126e4c8-5684-4b04-b105-b30314a9b4b8', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:00:05.777266+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a6d93f56-5a51-4119-a7f8-b54f4fcc503f', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 14:00:35.706348+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('133bf8d7-e093-43a0-b7c3-6d9617609d5f', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:00:35.71589+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('13cb5a57-7d3b-4214-8419-600b25c4363f', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 14:00:52.621203+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a3975dab-d87b-45b3-a6cf-9b37905705c1', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:00:52.630535+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('22ed0a57-3bdd-44fa-ba46-a5a8e4e91edb', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 14:01:15.062418+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('63d0dd1d-a03e-4c40-a997-cd5657bdb544', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:01:15.072185+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a279e9bf-6a82-4b4a-8fae-dcd903233eec', 'ChaLLengeR', 'rental:delete_apartment_cost', '2026-07-11 14:02:22.264389+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dc6ffaf7-dda7-47e2-9058-929c0c57c393', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:02:24.928532+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c54ad917-df0b-447e-b2e5-a53b4c099554', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:09:59.190416+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fa26232b-19aa-483b-bc0c-bbce94687684', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:10:15.312272+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('819cfd0a-c2c7-41c1-8cc5-141a4dac0909', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:10:27.439274+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('47fc7814-4255-4190-960f-941cadc73373', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:10:34.013226+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2b88ef2a-4e06-43ec-99ee-38185732d85e', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 14:01:55.094118+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1ffb2361-5e46-4ceb-8e3c-2c5358f20c25', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:02:22.27474+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5fa16104-ff09-4040-8444-bf32a02f46aa', 'ChaLLengeR', 'rental:create_apartment_cost', '2026-07-11 14:03:01.761874+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d1e19b48-00a9-47d0-9a4b-28132e2c9e36', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:09:59.203667+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8d08141a-4726-412c-922e-900b96e9fed8', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:10:21.39984+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a2f6f353-21f2-42f3-b754-dd11a7022296', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:10:27.44894+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b62f6454-d430-4f51-911d-f511b6be278b', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:10:39.724246+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('091ea720-2983-4deb-9f87-513b695265b1', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:01:55.105648+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('70f70740-79e9-447b-8d1b-f5716fe7fbd8', 'ChaLLengeR', 'rental:delete_apartment_cost', '2026-07-11 14:02:24.919593+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('42f8e21e-c931-4c7d-8654-25de67cf674f', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 14:03:01.773634+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ed1a5a87-c368-4cc0-9a37-3d8f6370c588', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:10:15.297325+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('111f7f95-d903-493c-9c0f-81c19a63d9b2', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:10:21.412281+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('050df1e3-89b6-4da1-acf9-09210d6e7ab2', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:10:33.998993+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('144a492c-235c-4a98-8fbe-a5d1243d74db', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:10:39.733681+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1c4acb59-7906-465d-9d64-75f43fcfc024', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:11:47.921206+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f515fcbb-2df9-4ff4-9315-3c62f40549d1', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:11:47.931997+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('abc41a71-c01e-4872-ae06-c27c864206ea', 'ChaLLengeR', 'rental:create_meter', '2026-07-11 14:11:54.241003+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('321a0a70-c674-4e95-9845-90ccc986e9a4', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 14:11:54.251395+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c2a5656f-7d0e-46a5-91ec-2e2acafaf3c0', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:03:37.791255+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fed4a4ee-5ac4-4394-8a16-a1f05045ac9a', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:03:37.915974+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('16ee1b21-af67-4827-82e2-1ce0856bcc43', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:03:37.920245+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('89684c46-eb2d-4d71-9920-103af872b19b', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:03:37.923636+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e241af5f-6d28-4e1e-a968-667d251c0e74', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:03:37.940126+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5bc98f25-3347-4048-aea5-5fa1ecb7c3fb', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:03:37.976657+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fca4971e-d1bd-4e8a-883b-99d15ee146ce', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:03:37.979547+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ebad0858-92bc-4e03-8e8c-fa09a031eb7d', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:03:42.436881+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b6d8c685-cb2e-46da-b146-9f7ae3dac5cf', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:03:42.564843+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('590603f6-cc3e-4ba0-93a4-5baa6d2c12d2', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:03:42.567224+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1d1ddba4-1203-491b-a0af-5f2da580a1bf', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:03:42.567552+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('013211d6-232c-4794-8453-503b982ffc7c', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:03:42.581529+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('76dc990c-d9cf-404d-80c6-7a47617322ff', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:03:42.634201+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bde8277e-0dd1-4073-908a-2acc0068056d', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:03:42.638178+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a5651735-6d05-4f03-887f-f35ad0fadf22', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:03:47.169163+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('24ab1890-8e31-4d0b-8b57-b16713989e14', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:03:47.318279+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d09a2e5a-3dac-4607-b869-ea41cb74b3b8', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:03:47.324489+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('77e4da4e-3fc1-4631-a99f-d0791dee77e2', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:03:47.323052+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('66487ab6-9ef3-4a64-afbe-8bf8f3e4e261', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:03:47.337056+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fd6d2041-61ea-4afb-9661-999138826788', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:03:47.387171+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ae3e656a-bb05-4fde-9dbe-72756ac817c0', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:03:47.393807+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d6fe7292-21c4-484a-a935-079f58ff35d9', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:03:47.54401+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('804e175a-12ca-4f8c-8d5d-34db9e7be5d9', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:04:21.876639+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('96f527fe-6088-40b8-9a5d-09f05b5658b8', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:04:22.018165+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c5f3d355-ccf1-420e-963c-32591d63e220', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:04:22.035235+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c6984195-cd58-4a48-9010-09f975a2d052', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:04:22.035009+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('36aad162-cc1b-41ae-9f40-0627359a4d5e', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:04:22.04308+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('251926f7-3146-441e-91d9-b3af3d69fedd', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:04:22.080518+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('80233c36-b9c3-4dec-9cf5-2303a965b745', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:04:22.095373+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('db785914-92af-48c7-9fd9-339fe6081ef5', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:04:22.1749+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('64b86b94-b98e-4ba1-bc33-58ec1bf4a36d', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:10:07.018746+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('316b620e-80a5-4401-974c-b53277b2ed9e', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:10:07.162654+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cf99da93-dfb4-47e5-b299-853d4b2d57be', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:10:07.172228+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cff935a7-80f6-4942-8e52-dee3055bd4b5', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:10:07.172644+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('00b26f0b-6f93-4763-a612-ff18c25f477b', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:10:07.183864+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('24840b93-783b-429b-8ba5-d706f216e64d', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:10:07.235722+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f21b2373-28ea-4828-b13e-626a4dcbf129', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:10:07.239075+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3d220f48-ebc9-4cfa-b9fb-96ea8ff3f85f', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:10:07.294969+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a511d2c8-1667-4162-8288-2b445bd458e7', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:10:11.870187+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('47777b69-cc21-46a5-bbc4-7e1e6bd71e2f', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:10:11.994662+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c3d134c1-0759-4fb1-a180-d1b6aad03b87', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:10:11.994836+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c5e7e756-6c51-4244-94ae-2cbaf9db06d2', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:10:11.994989+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('153cf92b-2706-4509-82a0-9eab611779ea', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:10:12.006724+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d8d5eb47-e66d-4858-8054-3e8408d103ae', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:10:12.049571+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d3654f65-b79b-4ba2-ba17-5067285264ee', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:10:12.136654+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bf330edf-f696-4440-8da7-87c18c77ab65', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:10:12.152828+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b2b4287f-3cc0-446d-a087-9773883fef72', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:10:12.155026+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e824d9bd-8515-46ef-bb8b-ad63ca759dfd', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:10:12.185154+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('faabc00c-111a-446b-8fb0-398c8c8b41a7', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:11:20.222483+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6c357426-9617-4cd8-9205-237662b57087', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:11:20.353446+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2f8ef1e1-99cd-4e6a-8996-c128a412252f', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:11:20.362404+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('37b0b6da-7fe3-4dc9-84d3-436345ac0f8f', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:11:20.364927+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2f029f8a-9bc6-48a8-b6af-902826a2ac2d', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:11:20.375971+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d3f1e03a-c5fd-41e1-9edf-c9049c142fd7', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:11:20.427537+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7b3c4e4d-a82d-4900-a97a-f00b8e799f40', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:11:20.429648+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('909a03d8-87a1-44f3-a605-911f0340e838', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:13:21.724827+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('926bbdf1-7bba-4c48-a9fa-4012442efdf2', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:13:21.842676+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('80401a58-e57e-4ffd-aec0-270356061f6a', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:13:21.85893+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c0dbbb78-a606-471b-84bd-e202e5cfe106', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:13:21.859781+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e61bfc1a-4f36-47a0-8f04-5b0ee5d09595', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:13:21.869535+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c279f164-7efb-4f39-9a43-e2dd795c8f0d', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:13:21.907594+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a1f39938-df44-4134-8578-4bf334a60f82', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:13:21.910006+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5236e80d-75e3-407a-9ace-c09d1055f57e', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:13:22.050613+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d44e7e1e-a8f9-4695-b59e-3afc7b679e4b', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:13:47.576439+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('49059824-f634-4ba2-8022-9d3d70b6cdce', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:13:50.685835+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fb1e546d-58ec-436b-a231-35a217d89f7e', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:13:50.68821+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b0b1f6ce-ccac-44fb-9abe-18312c98684d', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:13:50.707741+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7550b50e-2d9f-4d84-9b15-624d70d8ec26', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:13:50.721145+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('395b48ec-8267-4502-8f72-b8c9e7102d4e', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:13:50.732029+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6b50dce9-d026-45d7-a6ef-4300a5ccb95f', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:15:43.744507+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b330863b-4c14-49e6-832c-2267667cc1ff', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:15:43.827013+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dd91728e-6902-4633-a43d-10f5863e6a14', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:15:43.829005+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d69ca60d-8ffb-4874-b064-5ce519c236d5', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:15:43.852985+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4d270bc8-8128-4bf6-9370-a24ea1f2c7e7', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:15:43.867033+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('13ff46b4-718a-4734-9ecb-a94619c2777c', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:15:43.874607+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f5ee1fe8-00a0-4284-b7f9-9ea02d175049', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:15:43.886384+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9fe83383-0301-460c-8741-63b0a578f7e3', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:15:43.890984+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3a8cc8ac-b97d-4ab4-adea-502e5ef37adf', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:15:50.45481+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('943cf094-705f-4cdd-9dc1-0914a7e5f49b', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:15:50.493605+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b85f06e6-7847-4214-a572-029312615970', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:15:50.542759+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('028007b6-b923-48db-87d3-ae590e818738', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:10.829969+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6a8767d1-5938-4015-89d6-57fadcb880d9', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:16:10.873203+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('92db988e-86c6-4064-b829-88fcef0832a2', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:16:15.452694+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c9c2682c-d858-4e0c-8818-93090082a93e', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:15.606417+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('35f9fd2c-23f7-42eb-bde3-38e095a44570', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:46.642228+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7c9af055-ac1d-4d05-bc51-c6789d20fdaf', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:17:03.862467+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7dc66a66-9c51-4a50-8430-2ebfffad42fe', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:17:03.902922+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6e0c00eb-7356-4e84-9558-69f49963944b', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:17:03.929043+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('72d2f31b-9af9-448c-a189-0de525be530f', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:17:08.827861+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6fd8e319-9fdc-4ae1-8f49-87cd58d90e7d', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:31:28.537341+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b06fe213-542d-4e5b-aa01-17a04a03f601', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:31:28.571431+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('70a126a3-4e58-4e62-aa4a-42287fa7aee4', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:31:28.626758+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('21206063-0df4-41df-ad06-b81be629149c', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:15:50.362588+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d6b638ef-17ca-461d-8d42-f37ad975b3a2', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:15:50.512188+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('91caa3fc-d483-4351-94f6-26543cbea673', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:16:10.800873+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('445ed60a-3872-4c87-97f5-8568fb5a54fc', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:16:10.853799+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3200c667-5317-4bbe-a7f1-7d0c8f44244a', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:16:10.873247+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('80909603-2001-4661-94ce-9fd00d338861', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:15.545948+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a555a4db-59ca-41f1-9204-71dd2d57810a', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:16:15.614784+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ec79a0f6-7ca0-4648-bf56-c4b35124e248', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:16:15.636526+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('256816cf-c5e8-4a8e-9520-f098f586fb82', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:16:46.609557+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('730dcda8-0597-499a-862f-03caf868a381', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:46.630807+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5e27ed4b-3909-4935-a4a4-f1f03fe3b4a0', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:17:03.654307+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d6bd595e-0c71-47e5-8ccf-8cc8b0ccb1b5', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:17:03.872429+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c95ef5d9-a9ba-4062-ab37-18a751fd93a2', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:17:03.929464+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('96cf8574-3bdd-430a-b857-70d426a94ac2', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:17:03.956022+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b786d32d-3a1d-42bc-b57b-e3e3ef5a81b9', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:17:08.792188+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d365e297-3ae8-401b-93c6-fdbc58faa696', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:17:08.815485+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b13a95f6-1921-4bf3-aa01-ef266b26eb88', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:17:08.849299+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7b740570-e74a-4411-a030-7b3bfe6fb1f6', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:31:28.591809+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('39a15f94-f528-4211-8bd7-88a05b429abe', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:15:50.458035+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('67f5bcc5-60fe-4518-90f7-2f470d955014', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:15:50.522221+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('54b87463-8401-49ff-b078-f4c9781dbd9e', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:15:50.542546+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5ae68c66-111c-4c2c-a269-eb914dece977', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:16:10.712382+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dc0fe2f0-db45-48ae-a757-99d93fed8a03', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:10.793589+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7371d8a9-0931-4c32-adda-de23f8674aba', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:10.847951+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6312bb85-79d5-4465-90b9-d8d22c93b921', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:16:15.545792+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f656460d-a01f-417a-91dd-0e49c1465074', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:15.591632+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('991df4c0-58ab-4cd2-8d60-379ffb9e0615', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:16:15.63668+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4c9d14ca-bd07-479f-8ce4-95602e21d837', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:16:46.603176+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f87a0a4e-63b5-4563-9d20-f2bbdb847d0e', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:16:46.655611+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('99fcea9c-deb2-41ac-96d9-b5e9b16db819', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:17:03.955813+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7d65ce9e-3289-4565-b4d8-fa8dc8e224ad', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:17:08.683651+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7a6a62b8-c863-478f-83c8-5979dfe692c4', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:17:08.795122+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1f204e55-c6fb-4ff8-b3d3-d18d4dc9a8eb', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:17:08.832854+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('917f209b-cebf-49b6-9b18-7570335817fe', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:17:08.849012+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e9fd4eb6-8452-4c5a-90c0-755603917549', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:31:28.401434+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('edbd63f3-3b5f-4809-a092-062bc10afbbf', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:31:28.53751+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b1bda80b-0132-41f4-a359-d60a560f7650', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:31:28.601658+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('481132b3-1f9c-4562-b8ca-cf58865ff4c7', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:31:28.62655+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f974d1e4-f371-4140-8270-59729b21717c', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:35:40.486728+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f6c6cc16-03e1-4f75-9f0d-47232ed5acd6', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:35:40.531357+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a3e1e92c-393e-4694-b531-c04bbf19f01e', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:35:40.532171+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0451c2b0-f501-4dbe-b429-a8fba6d14919', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 15:35:40.535188+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ba42a5ad-4a61-4172-948c-bd3b61d09479', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 15:35:40.578999+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cdaddc1b-aae4-4649-91be-a43e58247878', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 15:35:40.578771+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8040dafe-680d-4ef2-bcf7-3cb86eb4fcae', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:35:42.568471+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ea648dfb-fcd8-43b6-b12a-be07ef655cf2', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:35:44.132654+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5f29a17f-8608-4512-ada8-913f55295a7f', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:35:44.132798+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('63934ace-5a9d-4285-9a20-950b6af9a409', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:35:44.146586+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('457e7d21-aaa7-4b1b-8120-c7ba95b065cb', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:35:44.156822+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3ca4f453-bb77-4aa9-a1d6-6a6897f77159', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:35:44.169398+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1d26de2b-72b7-4746-b414-e74505bb2ba7', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:35:49.87531+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bb3256f5-e915-4dc5-94b5-1e5bb0f2db7c', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:35:50.311835+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('be97c97b-c1ec-4017-adec-b3f11ced51f7', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:35:50.313848+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('116124a9-21b8-4dba-a2e8-d0dd0c1a768a', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:35:50.328195+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4fe7d9a3-2f4b-4be3-bf30-aab8e2015c4e', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:35:50.337021+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9b2b4cdf-5c23-4592-8165-1deb2a4fb51e', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:35:50.352873+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('423dbbcd-ce1c-461c-a26f-8647e3d6161a', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:36:15.650364+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9204b295-b7f1-4178-a55c-c68214e8ac2a', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:36:15.765442+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f5efa7fc-4176-454a-b637-d287d5d4fdc0', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:36:15.773234+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2e6a7802-37ec-449c-bafd-ddf07d837d45', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:36:15.845034+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cc6d1668-3ab9-49ab-b734-6352636dc1c7', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:36:15.861537+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9cdf4690-3a2c-4774-9f49-4ee42599250d', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:36:15.871674+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f6eecb70-0ce2-4d4f-8634-6fafe942c3ef', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:36:15.915748+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f6cc5e38-48c9-4359-861f-4ecde86c4dea', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:36:15.916023+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('546afad7-bfc4-41e0-b463-4bc5b334094d', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 15:39:44.507214+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b6d14c3f-4241-44f6-bb0b-207d10fbe859', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:39:44.608189+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c34d996d-01bc-459e-a960-1f6427fa9998', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:39:44.613708+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d8127385-2dae-4b7a-9218-31924ab6ef74', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:39:44.613984+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('23d8bb6d-3757-4931-ad37-1b6f263ce676', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:39:44.6412+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c4422312-c10c-460f-b76e-695772b88cd1', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:39:44.65174+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('94f9eee0-1c33-41d9-8d34-57c9fc6ccb6e', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:39:44.659233+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3f7a337f-1540-4440-a1c1-609b1fd7f619', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 15:39:44.668558+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('485c17f0-25e6-4db5-80c7-bdca1171e2d3', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 15:39:44.678829+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e87933a4-4038-493b-a97f-d13c94ccf68d', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:39:49.065413+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4ee15804-74b2-435d-89cd-8ee169e404f0', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:39:49.709382+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1251e1e7-b1a4-4fc6-bb2d-66ce438a44cc', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:39:49.709511+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('86fa867d-70e2-4aa5-aab2-618c907cc937', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:39:49.709681+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5a4a7b85-d722-4cb3-b678-c7e1e332ceb9', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:39:49.727786+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6b12f9a7-b5c4-48a5-9930-53a7b302910d', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:39:49.735962+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d339e1bb-f73d-4ee1-a634-4d55fe37d373', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:39:49.747649+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d88571e6-7f0b-47fb-94f1-1596d32beb33', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:41:06.307553+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8fda8f4b-d707-4bf2-be09-21b7374b756a', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:41:08.76117+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ce500e72-2547-4965-b331-5e7f94b0a4c1', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:41:08.765562+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('737d6c4c-7a13-40be-88d8-e7e38c3de1bc', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:41:08.765813+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('61a79bf2-cc64-4b6f-80ba-d32aa82b173c', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:41:08.780293+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('723c8ecb-0be4-4267-9047-30db03039476', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:41:08.789375+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('77678428-b199-4942-b703-92293528ee42', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:41:08.793193+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('edb13467-01c3-462e-b106-b6487ddd3528', 'ChaLLengeR', 'rental:create_beneficiary', '2026-07-11 15:41:13.408963+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8b5127e6-2a8e-4543-8299-6865a0830d2e', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:41:13.419739+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fd4fde80-8784-4e22-9ceb-8a3602c1ac03', 'ChaLLengeR', 'rental:create_beneficiary', '2026-07-11 15:41:16.907242+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fd7cec20-3043-4145-8bce-e1c3e0af50cd', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:41:16.917263+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('136e20f5-f49c-4991-a4d4-4b7c73baf2ed', 'ChaLLengeR', 'rental:create_beneficiary', '2026-07-11 15:41:19.577181+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('180299b0-f185-4b5c-8397-9346107c1d02', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 15:41:19.586512+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3d83da92-cd1e-4213-bb10-f36acf6ba895', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:42:34.830319+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('224b8710-43a7-42ec-aab9-6d1db7c4e916', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:42:34.844997+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f04c01a7-db52-47d2-9cfc-c344911fa72d', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:45:23.98699+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a1157065-91ed-454c-b8c9-f5cf9b53ff28', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:45:23.997999+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('76ae9d8a-590c-4d22-a677-313c971e83a7', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:46:06.989386+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e4648702-83f7-4cb3-96dd-094cac62462b', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:46:07.001253+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bc318b61-d919-4855-8410-7d3de70650a1', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:46:21.27044+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c6890701-43ad-4969-8f7b-acbe64278e97', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:46:21.280877+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dae3b81d-f22c-43ca-8795-287cf2e74661', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:48:08.518885+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('67fbe613-9570-4549-b1d7-d9aa574207ef', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:48:25.475276+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('27fdae08-896f-4011-9cfc-c9c5465f11b9', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:48:55.854868+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('38428831-4ab8-4816-846f-8c333354be44', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:50:02.433204+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('acd6ae13-2e73-4b97-b8a3-22c0ddb59bdf', 'ChaLLengeR', 'rental:delete_allocation_rule', '2026-07-11 15:52:18.183941+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dc6fe103-5318-4524-82d0-7959d2ed4b18', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:20.184117+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8ba1be2e-3b6e-4a1a-adb1-b203cf916b43', 'ChaLLengeR', 'rental:update_allocation_rule', '2026-07-11 15:52:35.307458+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('56249a0d-897d-4d63-bf68-6470d90b1575', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:40.768156+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9655d7aa-1c40-430f-877c-a9ca53d3f555', 'ChaLLengeR', 'rental:delete_allocation_rule', '2026-07-11 15:52:44.146052+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ed2e572b-6292-4779-aff8-457fd7e93264', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:58.037166+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('628e18be-1f83-471f-a126-f25918ced8ad', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:53:09.950945+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5d99f01f-e3b6-4691-b508-97aa97c4e790', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:46:50.06362+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('02e4b3b0-53a9-4ff6-802a-8ef43e04e8d8', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:48:08.531442+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1f36f4c9-053a-4440-a1f1-351f08a2e15f', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:48:39.87327+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('39779f71-da25-49f6-99b8-05bb6056f9ad', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:48:55.865335+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e8f5bef5-b6e1-49b4-b262-42a045909196', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:52:07.583053+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6e3ecb96-01aa-4663-960b-fae32b3de5f0', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:18.198255+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ba553a84-0083-4e8f-8e0e-2fb07815b50d', 'ChaLLengeR', 'rental:delete_allocation_rule', '2026-07-11 15:52:21.787242+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('751d6638-ca40-4623-87a6-be6b967ed6e7', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:35.320769+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7944a81d-f76a-4ddf-ba5e-7d60a414fa1a', 'ChaLLengeR', 'rental:delete_allocation_rule', '2026-07-11 15:52:42.453607+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5dca4ef3-a72a-4fd9-890e-3511b55c569b', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:44.15605+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('027dec71-b928-4930-952b-887ce3ab5ed7', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:53:04.123823+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1bb26c2a-69bf-48da-9e27-0cb110ab0da6', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:46:50.072827+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('568befcf-ed44-4745-87f9-b93c6a89c1e0', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:48:25.46618+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d2a6e34d-2c1a-4fa5-a50f-7e3865b352f4', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:48:39.88306+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6022d70d-c1b4-4233-83c3-4abeba2c6a7e', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 15:50:02.420268+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d8a48ee7-1f41-4b29-8f14-55e47940410a', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:07.592464+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9f1337e8-bd4a-43d8-84d5-69250d34c7c4', 'ChaLLengeR', 'rental:delete_allocation_rule', '2026-07-11 15:52:20.172691+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a06baa61-2d79-4c79-85ab-e004ee9410ee', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:21.797963+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6079ffd8-711d-4adb-909c-766c1030f6c0', 'ChaLLengeR', 'rental:delete_allocation_rule', '2026-07-11 15:52:40.755106+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1e9b313f-81b3-4d26-81c0-852aaca9c27d', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 15:52:42.467956+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('08f801e8-265e-4127-9f80-38b2ff6c3230', 'ChaLLengeR', 'rental:update_allocation_rule', '2026-07-11 15:52:58.026882+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('57d143fa-073d-4614-83ab-01dc6c2c2091', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 15:53:06.366661+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7526866a-5f1b-44e0-83ce-24ca0948bb2c', 'ChaLLengeR', 'rental:create_billing_period', '2026-07-11 15:54:10.378014+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e45dff24-a4f8-49d3-bde0-23003bea9979', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 15:54:10.42536+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('020d25bc-ff3d-42a3-a723-19efe19f576f', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 15:54:23.255778+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2c14ed77-3d3a-4dfa-a64b-d05ce142f635', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:54:23.275696+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2ba70649-0f02-4637-a520-d090533da70c', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:55:33.927415+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fbf065b2-3b5c-407b-a516-0c3ec9caad16', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:55:33.942027+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('54e53156-ba73-435c-9434-555054a1fc04', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:56:12.574485+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b09e7ef4-7586-45d0-84e5-1d4bb276cc1f', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:56:12.588383+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b1828488-e3f9-4815-bae9-8fe4c03a3710', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:56:21.570742+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7c8b1d7a-288f-4ceb-8c07-80a676eea277', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:56:21.580327+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1b239259-8287-4fa4-9b34-013d3a02afa2', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:56:40.413683+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('482c722d-785f-4563-b054-436edb61b597', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:56:40.424195+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('92b78413-d94a-4784-b40a-e6a6831066f7', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:56:50.981418+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('18915afc-4ed0-4f24-a7b7-99ff22e9c451', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:56:50.992+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('81c6f12b-0973-4f02-83ad-98764d95b391', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:57:04.721358+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('09f1b9ae-bbaf-4c89-88d4-592365024300', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:57:04.731334+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fb88640e-b912-4265-baeb-085b545e2cb3', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:57:17.980712+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3451db15-6bec-46b2-8a13-7a44bd102f23', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:57:17.991378+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b0c07d85-72e7-47b7-bd7a-bbf08d7c84eb', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:58:49.168617+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('51144b86-2ffd-413f-b0ca-b8d83b993026', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:58:49.179313+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2fae08e4-47a7-4660-96ca-1f279412307a', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:59:02.633936+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e4d4ec68-b13e-4fe3-8987-f544f16fbd41', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:59:02.644435+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a6732e0c-00c8-4d3b-97d2-ec244883edb9', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 15:59:14.086081+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dd9b17e5-f196-4579-b889-32041af4458c', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 15:59:14.09728+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e6fee63b-e2d4-41a2-9b74-94a1757a92c8', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 16:00:45.683596+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5646d71f-1400-41cd-8ee3-58050d95fa8d', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:00:45.729886+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cb269408-a498-490a-af2e-62b83ab262ea', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:00:49.481292+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1a70d12a-e8d5-4dd5-b3e8-4a9adcfe9a6a', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:00:49.497524+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c79336c1-2d3c-48a1-a5cf-5d02fd2b7e66', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:00:49.509039+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d54a237c-319f-4a16-bcf4-a41389fa1b1e', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:01:44.83074+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f4ef956f-c7ab-40d6-ad54-bf5c358623ab', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:01:44.845031+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('feccccee-c30b-4338-b5b1-55f434ce5255', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:01:44.844858+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dc000d48-12f6-4d95-a340-8675b2ab4ea8', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:01:44.85228+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6aaddd1f-e192-4b03-ab36-dc1acc8df9e1', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:01:44.892398+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('59c4a577-2ac2-439e-a7b0-3ea31f43ca32', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:01:44.996704+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('57ac9971-8974-4199-83e6-868a73495b1a', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:01:45.475387+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('30c891c0-8ab6-4ac3-b420-a66595ef4a24', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:01:49.127358+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('59851d3c-bd20-4ef7-9c9c-9d5e450b4602', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:10:10.421245+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3fed75b4-a59c-4d59-89fd-0298e0b52fd1', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:10:10.446155+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d8941bba-7bf6-4878-886c-7b45eb2a9d5f', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:10:43.597372+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('764f9f88-603b-4a48-b820-346d8d114bde', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:10:43.607007+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d16460ec-2b8d-409b-8573-6eb82c5301b6', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:11:33.498489+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7c7d0209-8072-4d90-a61e-f53c1aff1580', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:11:33.510121+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0fa0dd5c-bb7b-46b5-aef7-772247f12f76', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:12:01.051415+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('66729b34-e1d3-448a-bc11-59fa0ab62873', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:12:01.068005+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8f4644f2-6244-4a91-a274-51b2e4254d49', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:12:41.647635+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ecf34060-71c2-474c-88e9-c9bbf4a0929b', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:12:41.658054+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a84a4d58-1355-4520-b57a-a948e72b117a', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:12:41.670501+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('36da0bc2-0f4d-4f4b-8cc6-59da850bda70', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:12:41.675339+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2eb788df-ad5b-49bb-9d29-2555729acd12', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:12:41.708895+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9c0d67d0-066f-4943-b0ff-6c349a130a1c', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:12:41.724263+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9a82f6e9-eb61-4d2e-9956-9b166d5da277', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:13:14.442116+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1b999385-1cbd-4e16-acee-4b2dcba782e3', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:13:15.517486+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3361eb1a-c5ca-4d18-892e-5628b60cb821', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:13:28.058461+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b3b5d9f0-981e-48a9-b6f5-5b506541c8e8', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:13:28.071789+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3ca83bce-21bf-465a-a9d2-d342e584aa01', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:13:29.638904+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e99a63fb-390f-4607-b316-c10609f28fa6', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:14:26.329622+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a7cf570b-c661-44b5-8173-6b2c180cc57f', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:14:26.3315+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9639305b-3f18-4313-9d62-ff40e3192b5b', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:14:26.337121+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ab26ddfd-1258-4d8b-9cb8-f2893e989181', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:14:26.38403+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fd2d3c75-dbe0-445a-aacd-505b44737e2a', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:14:26.382144+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2ab47d31-e8ad-42f2-9b6d-eca41a90f929', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:14:26.418718+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c8f7fc7d-608e-4056-bfdb-a55e54810d97', 'ChaLLengeR', 'rental:update_tenancy', '2026-07-11 16:14:40.85631+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0b2ab413-1df5-431a-aeb1-5851278feaaa', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:14:40.8662+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('90fb95ac-ab6c-4d82-85d6-d3ff48dcf5fe', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:15:05.541258+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2287912b-fb7f-4b5c-b819-a547879a5754', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:15:15.498086+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d2ccf97e-9439-4a00-8703-cd205dbb161f', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:15:17.510138+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('28a69b29-2788-4d76-aefe-3c90a081ba3a', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:17:12.811588+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a6f35218-46b4-4c3e-8055-6a5ae67ee3f0', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:17:15.472717+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('85ff50e7-cddf-448c-8767-14aed1d04476', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:17:15.488116+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('648310a4-b978-41e4-b206-51000bd46037', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:17:28.6653+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('96f4aa1b-bb0a-4c8b-8ece-792d07ad5b48', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:17:28.675694+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cb4a51bb-a8a0-4de1-921b-fd67ccea4c96', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:17:29.414872+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ea7cba0a-a3fd-4453-a69b-e3cdbd03f1ac', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:18:08.535494+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f8cc8d27-778e-4bda-aa6e-a2dda759a0c7', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:18:08.590293+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('91785fbe-54ab-49a6-9e23-6c01b8241296', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:18:22.147994+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('57a315a1-26d0-4688-a2d7-6e238baa1819', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:18:25.924658+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8495506c-4d86-4b3c-9a69-8666b35473c0', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:18:42.141607+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a4cbbbc3-f508-4788-b6c8-c5e807ed51fa', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:18:43.963409+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bfbee73e-c395-4028-a968-ae3076554196', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:18:45.537127+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('24ee5aee-5399-4172-a5cd-861203e147db', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:18:45.606018+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e5ae8fde-63eb-490b-b72e-54ed520150f6', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:18:08.539694+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8ddea9a0-bf4c-49b1-8265-54f81035adfa', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:18:20.094255+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('60068288-4d78-4c90-9bbe-085cf271968b', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:18:22.150164+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7b1225df-f7e8-4cb2-8f83-a457f19833e9', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:18:27.123392+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('491301d8-0f81-4cc9-92d2-7589ae7a2f75', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:18:43.939774+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d70a9022-b12c-40e0-acdc-6500cdc9a37f', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:18:45.548183+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('46f4cf55-0bc4-41a2-a52c-c55db47d158f', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:18:08.540995+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a7885f59-c4a3-474e-b553-ea900e9139b8', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:18:08.588583+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('065ca289-cbd4-4927-bc2b-40e7b42014d8', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:18:08.631023+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3bdf4c60-da6d-4aef-86de-65ad09324e9a', 'ChaLLengeR', 'rental:update_tenancy', '2026-07-11 16:18:20.084344+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9134f459-739e-43dd-a986-89f738d77de2', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:18:22.147798+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5fa61394-1767-4d31-85cc-ba3a2b341fa3', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:18:23.543121+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('836b6725-f1aa-4997-a3ee-a06273c4a064', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 16:18:42.089481+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('997894d9-fd46-4e07-922c-f222e0761da0', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:18:43.950891+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3b16c78f-c9cb-4368-9e7e-234173028680', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:18:45.551148+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dd147f11-3e44-4c62-8208-2e579140a072', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:18:45.596156+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('203c71be-e01e-4eb4-b6bf-030527860e47', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:18:45.601672+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3dfba7c7-5ef0-447f-b311-b5556749f9ee', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:19:01.936709+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('91db566b-ad03-4147-be33-2b47e165c1c1', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:19:04.395708+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cca92e76-0b82-47f8-8396-9167a71c14d2', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:19:04.394262+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('747f26c7-5127-4584-913e-727424116451', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:19:04.395858+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9b70ac1d-640b-407f-bf2c-ba48f1aa142a', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:19:04.447937+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ea100145-ccff-4742-8637-badb51060eed', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:19:04.456362+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6c955fbf-7041-4d7a-8a26-fe84d732f81c', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:21:28.802906+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fee6222f-22f2-408b-a320-e9cb85ed0d88', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:21:28.815836+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9e0d83c4-1dea-4f52-ad6a-cafdb90895c2', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:21:30.430822+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('86287d3c-7f44-48fb-87b1-418b6889f33d', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:21:31.579234+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('46cfd406-88ef-430c-b4d0-c2287fbdd8c2', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:21:32.621727+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6526c21f-06a6-475e-9cca-3d4fa3207db7', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:23:24.1281+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b2e6bc73-c8f9-4343-8279-1d2d10c2797a', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:23:24.138492+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f3346287-2cb1-4a11-8fb7-501ffe1f4ba9', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:23:25.495515+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('90d28975-9ba6-4b56-a862-8d09dde416c6', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:23:39.856207+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9896ad14-c06a-4761-bddb-2d4210ec3646', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:23:39.866037+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d7d850bc-a8e3-437c-a111-d474e4eac91b', 'ChaLLengeR', 'rental:update_meter_reading', '2026-07-11 16:23:46.395098+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f550daec-92d8-410c-af1d-e23ede44265a', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:23:46.410172+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6239c4ba-7e32-403e-bbda-c21b4c9dbbfc', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:23:46.876455+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a2598f2e-fcdf-41db-83d4-2e4d3d1f1766', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:24:00.827322+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('00dd202a-f4de-4559-99b8-79f3d7d80ade', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:24:00.827169+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cf4decc3-099e-40c9-a899-5fe81819b7cd', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:24:00.828665+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('28083b17-9686-4866-8a29-69f0c3da869e', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:24:02.517713+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4e834231-156d-431a-be7e-4b0008958986', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:24:05.010562+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('432a2e35-370e-402d-8135-ab9071539ed6', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:24:05.025131+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7779bdb0-d030-49fb-b5f3-83ebc87ca3ee', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:24:05.035092+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('909e3a60-885a-4ea7-833c-158630a936be', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:24:05.045459+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ecbe2cfb-4399-423e-9efb-e9eae4c01bb6', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:24:05.066339+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('850470da-3f5a-491d-b983-b1ec1cdb59ea', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:24:05.073781+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0f19b613-8666-44c5-8c99-5bebc90660cd', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:24:26.630762+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('43f724ce-8156-4dcb-bab6-23bffa76a3ef', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:24:27.185036+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('44c39eaa-0f9e-4de4-8c65-2e158bb72974', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:24:27.194955+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('88e95f8f-a5c2-40b8-a01d-c041b5410329', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:24:27.197101+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0cbfe69b-0330-4cc6-a036-a52835e8321c', 'ChaLLengeR', 'rental:update_allocation_rule', '2026-07-11 16:24:52.514155+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('23c32035-490e-4649-9916-3f1069cd5c1a', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:24:52.527115+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1b8bb338-dd28-4acb-b858-80a045786342', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:25:41.095009+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('df633ae0-76f2-4991-afa8-6b033149c49b', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:25:41.104379+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dd0a26eb-2c67-412d-ac75-2e23f8923b05', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:25:42.890142+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('53632dbb-3f02-4dd9-bcb1-48650d2cc847', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:25:42.898636+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7ab343a7-9df7-4217-b5c0-b8d0e77814b9', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:25:42.90461+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('87883f2c-8e80-414a-9aa6-cbc87eeed4ac', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:25:42.946222+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('29de7186-4a9a-4b0a-bfed-05c09fc918f4', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:25:42.945483+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('06dcfc87-c4ff-4dca-a017-18601658a865', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:25:42.952587+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6e576418-4554-4446-97eb-a7429fe3ee83', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:25:43.902093+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('44fd3237-53aa-47c9-a7cc-e4c2950f4ce0', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:25:45.11928+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('af247f57-b8ec-44ec-89b5-c90ad702843a', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:25:46.985015+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('266c811d-8c76-4c98-b7cb-7e53de9b8b49', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:29:12.350214+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b4565480-ff8c-46e5-9ab9-3ab8634114f1', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:29:12.364323+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e8db47a8-e258-4530-82c5-14338ff28b70', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:29:12.364473+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4a5ad806-7643-4f2c-80e1-26220de53ac2', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:29:12.408205+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7e2a3dbe-e3cb-42c8-aec1-6dbcdfa541f3', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:29:12.407977+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5337d458-35b2-4eaf-b0d9-c075168b5b9e', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:29:12.44905+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('80ff7e9a-1374-40c7-9b02-12b6007f07e3', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:30:18.213337+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fca1b660-a3d3-4192-a866-ae84a1f3cd16', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:30:18.220147+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e25711bd-382e-4557-87f8-7589110a69b6', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:30:18.21934+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('41b9bbc1-75b8-418c-879a-a8a69a33c638', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:30:21.562979+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ab3491ee-4289-46b2-b2eb-1bf73128f69e', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:30:28.584618+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3b843b44-66ca-4495-9520-9fb087c02a83', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:31:42.437456+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cd49f7fe-be85-4ddc-8cf7-95c1eebc26c0', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:31:42.455342+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fa217c74-edfb-4e11-b48a-90dcc090dc6f', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:31:42.454889+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('79c4c621-cc88-47d9-9353-ba8eb417f303', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:31:42.470502+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('62a12975-eda5-4c46-8085-8231321af8dd', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:31:42.520967+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6ffc1800-c2ae-4409-90eb-054823ce9f06', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:31:42.521163+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f2ed3f38-37ae-4954-afd0-622333075ad6', 'ChaLLengeR', 'rental:update_tenancy', '2026-07-11 16:32:02.093144+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5e3e404c-fa3a-4fc1-aa30-80bfab007c65', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:32:02.104296+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9bf49a46-fcc1-444e-9c36-7013714220dc', 'ChaLLengeR', 'rental:update_tenancy', '2026-07-11 16:32:23.499752+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d13d017a-1b3a-433e-a43f-9bdef076e70b', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:32:23.509659+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a110c657-7648-4e13-89b6-1a093d74594c', 'ChaLLengeR', 'rental:update_tenancy', '2026-07-11 16:32:38.022892+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3585799f-b8d0-4101-ab1a-e0271486349e', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:32:38.032979+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c8c4b6a9-ec43-49a0-8033-ff68ab5b577c', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:32:39.343466+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('61f7d307-130f-42ac-887f-1a013e5e6323', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:32:39.350083+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e2009935-335c-42e9-bd7f-27528678dc6b', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:32:39.351189+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('df1ff7fb-16e0-43b5-91cd-c0f36d4267f7', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:32:39.904323+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('194f8b5d-9310-4dd5-ad37-a46c8d38d139', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:32:40.869129+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1adde3a9-23e4-477f-8265-95cc5a4f8680', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:37:55.183072+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('66ef1ba9-4deb-4750-a7c3-b51db3609987', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:38:05.436539+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('71f99ad2-0d1c-4c00-9aaf-ede04df998a1', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:38:09.210093+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7b7c8a7e-f801-4a25-8039-c261c794986a', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:40:30.011069+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b4e13235-4aed-4dc2-92ee-e0013f112bcc', 'ChaLLengeR', 'rental:update_allocation_rule', '2026-07-11 16:40:52.211322+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6d1ea7ba-5605-4a9a-9b36-5db95f88484b', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:41:18.979737+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('336fd19b-9685-4d51-b59b-c1e7885b5cb5', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:41:29.319329+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('66092dfc-6158-4c4c-8ebd-b29778458f02', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:41:39.389392+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cc57fe9b-9f29-4a70-93c1-855b0e203924', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:32:42.11721+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3f960c5a-875f-4fc3-9e2a-b239c4520301', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:37:50.210306+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('43b69581-b547-4f6a-bcc5-cf2dcf94e815', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:38:00.219745+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b3841036-ad6a-48f0-9597-b4b1c5179b71', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 16:38:05.336221+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3336d32e-eb8f-4c06-89a6-87811ea0c0fb', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:38:09.179575+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('958260d2-50ee-4447-bd3e-566e2cd78a48', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:38:09.195555+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e5b598d4-8241-4074-bf47-babada6be4aa', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:38:18.290718+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a529e7f6-4b90-43f2-a816-954aeaa60ee4', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:40:30.011191+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f6704ebe-1a37-4069-8c0d-b0f125ef1337', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:40:30.010931+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1b9e3560-30fd-446f-aeb9-6cbe46aebe5b', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:40:30.102786+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dad3fc5d-a678-4282-b8fc-5575d137862b', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:40:52.22247+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('563c5f79-4dd3-4335-80b4-0cef0a98f45f', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:41:18.970275+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ec52a7a8-9998-43d6-aede-f28ca2be3457', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:41:25.090705+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d9502d63-faf8-4827-87d5-b3831dceec28', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:41:28.347889+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('62ec03a9-fdfa-47b7-b122-560e221b27b5', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:41:39.380418+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('df85e92e-79b5-45f1-b402-4be286801a92', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:41:39.390707+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e0c5cf3b-6305-4445-b99b-fb04825e500e', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:41:59.216107+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5aa01800-3a6d-4adf-946c-700036ce6edb', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:41:59.228318+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3677c449-bf82-43cb-aa83-9e0629110957', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:42:38.290764+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('52a87949-2f99-4255-928e-790dfb4e841c', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:42:38.301201+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a9d8ec72-d816-42fd-8e53-0d2c5b528d04', 'ChaLLengeR', 'rental:update_allocation_rule', '2026-07-11 16:42:53.575624+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a5df91db-af42-4787-a0b3-ddb707cc9052', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:42:53.585404+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('06d8c2dc-6baa-4912-bd12-ff2b764177ae', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:42:55.206746+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c28637ca-2905-4f45-83bc-24c5d23e48ff', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:42:57.007778+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('04b109fc-8fd8-489a-b7ac-e8c0f7522385', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:42:58.769202+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fd963ada-b51b-41a6-9b31-a0b15819e985', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:43:17.270327+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('dcd93761-0a59-444c-9e74-f5dce5b7429f', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:43:17.283581+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8a671fc4-5822-45f2-a8b3-cf8942ba25d7', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:43:17.283295+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d3107127-7546-477a-b411-99974d32a66e', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:43:17.288558+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a29761a7-6e30-4f48-849c-d5539f0f8fd2', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:43:17.330392+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('60e9da67-2ff3-44fe-8571-4bbe3a3d2db7', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:43:17.333101+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9a327d34-5992-4fb4-ae9a-3309d2da965c', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:43:17.349318+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a7dcb731-f7e5-4e76-9adf-81eb03744438', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:44:20.693041+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0f70ad94-7116-4098-b180-536c983a741a', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:44:45.115966+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e8ce3cf3-8267-4482-b232-ca90185fad69', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:52:29.711594+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('45692d54-4c2c-4c41-b354-66961d481b8e', 'ChaLLengeR', 'rental:close_billing_period', '2026-07-11 16:54:49.68485+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('03b9f1da-f588-4db6-9f49-1ca4031ea0da', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:54:49.793718+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('30df955a-debe-44c1-9f8c-58c408ea402d', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:54:56.181674+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4108b9b1-a6a7-4c17-93de-e1e89d4faef3', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:54:56.187662+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8142b57b-feac-4d39-8b11-1d6b0fd472ba', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:54:56.199068+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6f0d5c17-5845-411c-9420-c24fa399d0a5', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:54:56.205356+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('deab42b4-a510-4a60-ae7b-91edf9db63c5', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:54:56.237278+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9ee025fd-1acc-4f4f-8251-cace02473407', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:54:56.240677+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e5b1a9d2-3c83-47d8-b7c1-e47de76bfb7c', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:54:56.33555+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('39fc0dee-0118-4fc0-a0fd-c59f9af8357e', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:54:58.60381+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('86b80afe-01c3-4b60-8c9f-0c2bc29ac301', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:54:58.609928+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('aec0f884-d47f-4997-bc53-8239051def05', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:54:58.611625+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('14373922-39d9-4aeb-8ae8-f3925c19ffca', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:55:13.928401+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f8b767d8-f258-4381-9bb6-2586c5ce5d15', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:55:15.126224+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('455cdb74-c5ff-47be-97e5-25de5b8f4d99', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:55:16.718281+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('55c3b4d4-32cd-43e0-b3ae-93cc78c7f2a9', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:55:23.991005+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4ed7c9e0-0325-47f1-9065-b48da30d0523', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:55:23.995269+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2088fa3b-7918-4b94-9738-de36cd44eeb2', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:55:23.998688+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3284e16a-d918-48cc-a500-8b77bac63c03', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:55:24.039348+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5f0bd86e-85f0-4550-af9d-fd67cc200b36', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:55:24.039593+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5b4463bb-747c-4c98-931e-4d6b025486a0', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:55:24.173294+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9d41f044-e958-46c5-8873-4b7a848651ed', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:55:36.042874+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bf5dceaf-2987-4572-90e3-73d07c1d083e', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:55:36.059488+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('85cff659-81a8-4465-ae46-0c12f5c65c9f', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:55:36.059944+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d14ea64b-0f74-44f8-af1e-e11893884e65', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:55:37.804336+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('39da50b1-cb0c-4b0a-80ae-3153b6942af7', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:55:44.859193+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bba103b8-3cf2-4dcf-b138-a68f2f323c1d', 'ChaLLengeR', 'rental:reopen_billing_period', '2026-07-11 16:55:47.85812+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a804b91e-8535-4976-90b4-38b2f3477d50', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:55:47.879348+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('039f6333-fea7-4829-b038-c210a8357dff', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:55:47.92545+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7e56d3db-5014-45ff-9239-cf212bc4be51', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:55:49.365357+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bc1aa512-86a0-4dc2-a0b0-423c11a84696', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:55:49.371002+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('326c76f0-0769-4085-8a87-0207641ec31c', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:55:49.379321+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('be712794-8623-4e32-9eee-f3d2858eb8ce', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:55:49.382468+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c40351ed-acdc-4c28-bac4-15429a56feae', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:55:49.421593+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('17b6a658-7963-46bb-ba2d-0330302661dd', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:55:49.421764+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1696e58c-f7b7-4040-8622-69c7c15d79c9', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:56:23.447102+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3700f63b-df4c-4d55-9385-21671f6a94fe', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 16:56:24.952172+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4417fd01-7b93-453c-9ba3-0fff9756b799', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 16:56:25.673954+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9be9f3cc-e640-4b70-81cf-4a6ba3dce411', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 16:57:32.37699+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7d7eaae7-6cdb-4b30-a5a9-01f3d5732136', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 16:57:32.386868+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4f28d0c6-4fcf-49f5-ba94-79232884dd88', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 16:57:32.398671+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('68a06ba1-70ec-404c-8c98-b8a259f5fa45', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 16:57:32.399062+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ef96433d-914a-4d8e-a2f0-e234b19ac6a8', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 16:57:32.406703+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('63cc0d22-136b-4e13-a903-89303aa85f6e', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 16:57:32.432828+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c712aaad-14dc-4cb0-90cf-65cf103c7b49', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:57:40.600529+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b96d721d-be66-4197-97c3-b2790ff1fce7', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 16:57:44.983698+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ea109e45-3c94-4101-bb50-20c742c33948', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:57:44.990852+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6375c44e-af4d-40f8-bb49-7f8046248acc', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 16:57:44.993232+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('81ec41bc-a23e-423f-ba3f-c7ee0d11a9ff', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:58:52.842324+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('286ce77a-8950-45c3-bcd7-239cc57574cf', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:59:20.426447+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7eb968b8-c940-4dca-b787-4868f1151f31', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:59:56.266298+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9a9af5b0-2644-4ad5-aed8-755a1df37319', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 17:00:01.104708+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('63957ed5-d05f-4057-a7bc-7d0e8f7e4ec0', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 17:02:18.680273+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b6b710db-1b80-4b36-87b5-3e632e896b93', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 17:02:24.6365+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('87c7a977-336d-4b4b-9fc6-959c2d037a4f', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:02:24.653673+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fe7901ff-2657-4afb-9a5a-2e5e52d60c7b', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 17:02:25.054004+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2f7e4f5a-fbde-43d8-9743-be253c407adc', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 17:02:29.009024+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('931bcecc-4389-4a9a-ac38-b77e915a6d63', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 17:02:29.916631+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bd05f643-5da0-497a-a1d9-d40942ba9622', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 17:03:19.464195+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6e4ab6c2-5354-4671-b2e0-a73f3750bca4', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 17:03:26.065595+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a040f007-5b40-443e-b9b9-a7885dd4204e', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 17:03:27.465734+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3f3523d1-dbb4-4de0-80a7-652af7979269', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 17:03:27.485098+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ddcf2df4-b3a5-4987-bada-76dbe410a180', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:58:52.85338+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('da7abe3e-d36b-464e-8615-e9efa816c13f', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:59:38.679331+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('25278348-661c-42cd-85cd-a859ccc8e68e', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:59:56.275987+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6f5e138b-c398-43ba-83ca-8eb48c0d5b35', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-11 17:00:02.505105+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('65378bb0-a4d8-4613-b5b2-b50c6bcb2179', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:02:24.642813+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('db6932db-068c-4647-a2d1-2aeb66f6cd7a', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:02:24.659295+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d6dd6347-e33d-4505-8b0c-7480ed6b8f2d', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 17:02:29.010697+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('94a5b59e-031d-4fcc-9701-7b16022a5395', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 17:03:19.465692+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4be7a302-23ee-44d3-bf46-04204b3c0797', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:03:27.487247+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8ddc1ea8-b7fd-422f-859a-2c179a4d5553', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 17:11:25.488521+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f9e46f0f-8779-4e4c-8b2d-1fe03f076650', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:11:25.50241+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b82dd476-b43b-4ffb-83c5-ac78ee556cea', 'ChaLLengeR', 'rental:create_allocation_rule', '2026-07-11 16:59:20.414703+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('229da718-ab50-4668-8346-8adf3601ce3c', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 16:59:38.693389+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1eb30a3d-4407-463a-a260-6b29045195a0', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 16:59:57.86429+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('65dcce1b-17b9-487c-95c4-f897a5170b6c', 'ChaLLengeR', 'rental:close_billing_period', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('22d61e8d-148a-4bbc-b8f6-64f147e0390b', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 17:02:24.654039+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a4e00291-f8f2-417a-a580-67e308929952', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 17:02:24.695725+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('70052572-bff4-4a66-b994-2f5367477397', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 17:02:29.000593+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5e423abc-a5d7-4e43-8e9f-2880abfeed8d', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 17:03:19.45526+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('733d9124-4793-47ec-8246-94e0c758d4df', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:03:27.475846+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b358f353-6440-435d-bf96-c7221295ea99', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:03:27.520861+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b783ed43-7148-4838-89ae-d25ab24b07f8', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 17:03:27.528087+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('36408d1b-c075-4821-a220-6d093342a927', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 17:11:25.384109+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a89ce413-cf9f-497e-94c6-7b78f3e00051', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:11:25.489408+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('13fd94d2-b76b-4856-aae7-f26c8f34f438', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 17:11:25.491207+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0316b9ed-af90-436a-8b4d-3558e5e48c9d', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:11:25.538683+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('048cf7b6-b4a0-4a9e-be2e-a7984fedd2d9', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 17:11:25.539381+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e66dba7a-cfca-42b5-ac96-d087a0e52031', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:11:25.571871+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('207d3e07-d933-4c39-ba01-9d6f7b7202d6', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:12:52.977837+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bbd680d0-ba31-4a08-9960-6beb4f29fb3f', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:12:58.041634+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('5f4ba415-4070-40c5-a6ea-f9452ce3b2db', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:13:03.078669+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c9f7d18f-b8a0-48bf-972e-977f9bc2b7f6', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:13:22.29621+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7dde825f-3028-4594-b3d0-4b2dac906219', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:13:27.351672+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('570ee545-0156-404f-9154-4dfb755dcadb', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:13:32.385747+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('58088f05-24f2-47c3-a59e-21f3602f6f55', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:16:00.476864+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c005ca80-cf7b-4c78-80c1-e6cb6a925963', 'ChaLLengeR', 'auth:automatically_login', '2026-07-11 17:16:31.546686+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6bbad5f1-271e-4165-9a87-a3715b1b2b3c', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 17:16:31.684135+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('094995cc-ad4f-4c39-b5e4-bde745a66cb3', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 17:16:31.693983+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bddb344e-de3e-44a7-9547-122eef270ebd', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:16:31.694285+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ae8da913-173b-4a4d-8a48-321bcefee7cd', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:16:31.708112+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('da09a8ed-f759-4a47-bad8-1a907a11d26a', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:16:31.739312+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9742f686-020a-4683-b3d0-d9b808935b71', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:16:31.801308+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6734d78a-cccc-4c0d-bdc3-32c60ce6fd57', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 17:16:31.840761+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3f633ca6-d91f-4245-89c0-49356c4f8be5', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:16:38.107673+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('976b99dc-0adf-45f8-98a1-2e80ab3ceecc', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:16:39.796284+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ad932b5d-e69e-461d-bd33-d989d5d80660', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:16:39.79642+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('375b52b5-e7cb-4c14-b95e-db8f947e0688', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:16:40.4199+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('95a1ca03-3bb2-4005-937c-fe20790637a0', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 17:16:53.317655+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4ffb8eb2-c717-40ec-a363-301e0708c893', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-11 17:16:55.081332+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0a10730f-fe36-47fb-a719-3b025a14ea9b', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 17:16:59.328913+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7636603a-5aff-4329-9d56-86cc9b8dbfe3', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:16:59.339181+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ed1020d3-9590-47e4-b24d-34187169e317', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:16:59.349786+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f3bbe6b9-2061-4193-b1d5-09e5581c410d', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 17:16:59.350088+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bbc8e90b-7117-48e2-a29c-c519f9efd975', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 17:16:59.358085+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ee6fa3ed-f3a1-4aab-b6df-585965cc2eee', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:16:59.388824+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('11431c71-c4c3-43e6-9bae-401a1b4b90e4', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 17:17:00.206762+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c8387978-1905-41ee-9da3-3e83b2e2ec17', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 17:17:00.206888+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1da867ed-9bc0-484b-9d2f-5592dcd79f57', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 17:17:00.206636+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('88a02053-29a3-4ecf-90c5-5d1dbe4f79f8', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-11 17:18:05.537458+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bae8b87a-9d1a-44f7-8819-47b0af5f2821', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 17:18:07.083562+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('fcedc15c-2d2a-483d-b5eb-e926228889b9', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:18:07.089894+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7a4c8ed5-7cbf-4ca6-aef5-81bb97bbf7ee', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:18:07.100741+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8ae92ee7-6114-4af5-b1b4-41799b094a4f', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:18:07.106913+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f958ae09-c753-4475-8ece-0305e4b33965', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 17:18:07.110352+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('6f272512-04f3-44b7-83d3-fea0e0aff6b0', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 17:18:07.139157+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d7a80b37-c970-49c6-b916-c393d0f08689', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:18:10.086655+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cdfce41e-c607-4a0f-8492-ba92348dc70d', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:18:15.297082+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0ddbcdae-b718-461e-bfe0-ab4100c3d289', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:18:15.297433+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f36f828d-19f0-4655-8ee3-58f1e7d8b232', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:18:17.475223+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a067b2a2-1034-46e3-9889-dfba67c3bac3', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:18:27.009494+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('8a38038c-a623-403a-823e-dc0df6a44758', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-11 17:25:57.787572+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9dd227aa-9dbe-49c4-9aeb-9de33f943131', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-11 17:25:57.828309+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a1dedef3-a58d-4ddf-9943-efdabbe14ff5', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-11 17:25:57.828036+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e5627c5e-b83c-44cd-9fc5-9c24491ed6c8', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-11 17:26:45.746367+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2ea89657-7df0-450c-b59e-5b3e9a7515a9', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-11 17:26:45.758049+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1378a85c-a9cd-41a1-8412-a27f5d4bd13f', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-11 17:26:45.762257+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c7b87351-bf54-400e-a5bd-bb7bbfccff07', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-11 17:26:45.801217+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('22b0f91a-e39e-479d-9670-4d0ab0a9379f', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-11 17:26:45.90961+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4d4f674e-23a0-4a39-a600-164fb5f6d0af', 'ChaLLengeR', 'rental:collection_meters', '2026-07-11 17:26:45.910031+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('25829925-d21c-4360-8010-d63fc2970392', 'ChaLLengeR', 'auth:login', '2026-07-12 11:20:44.546125+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bb1468e8-e516-4579-800d-1090cc54cbee', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-12 11:21:17.493193+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f48cc59d-0a9f-49be-b3b3-6eaba154eddc', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-12 11:21:17.517037+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ad873900-c8d5-4d9a-9866-2d9a9516a6a8', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-12 11:21:17.553011+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2c3206ba-d77e-4e8c-9804-efdaccb756cb', 'ChaLLengeR', 'rental:collection_meters', '2026-07-12 11:21:17.573238+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('68805f8e-aa8f-441e-9f72-f864a4d6da55', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-12 11:21:17.5721+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e6b81745-61e8-48da-885b-ae916b0f951d', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-12 11:21:17.634016+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('78a28b6c-b6e7-41f2-911e-31580ae47268', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-12 11:21:17.643019+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c0fd4055-8ab7-48a3-93fd-615314ec8be8', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-12 11:21:17.764738+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e9131728-a6c5-470b-b256-7a54ebb3b343', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-12 11:21:22.108315+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9c06b653-d821-4256-befc-2f2d43dc3d82', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-12 11:21:26.150526+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3e23b656-99f2-495f-a705-94723145f497', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-12 11:21:31.693218+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('32a344e0-6edf-4776-849a-fdb68b2d4a63', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-12 11:22:13.231036+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b5fccddd-a904-4f19-906e-bba376e03277', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-12 11:22:13.241373+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('f242045d-54a7-499f-bbee-85bd43aa702b', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-12 11:22:13.253428+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cf6a9e7a-4534-48d9-ba6e-59746eff8fe9', 'ChaLLengeR', 'rental:collection_meters', '2026-07-12 11:22:13.258201+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bdb2c2cf-83f6-4fe2-b1c5-18dd35ce9b04', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-12 11:22:13.290613+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ef8169f5-e323-4bbb-847a-316346e7a7bd', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-12 11:22:13.390334+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bc39edff-1956-47dc-849c-523a8af3633f', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-12 11:22:52.298045+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('32b0f2f3-62bf-4985-8bca-9b15d286032d', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-12 11:23:35.258485+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4d862fc8-3344-4e6f-b96a-4e656b60a917', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-12 11:24:12.178038+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('45fa94a8-05c7-4d52-8c89-2dc72b1183d3', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-12 11:24:23.60663+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('eba0ecb9-8edd-4d92-aeac-3ac11b288231', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-12 11:24:49.785956+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('930c80b7-297a-4692-a17d-abc693216f42', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-12 11:26:29.43255+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1cbecc2e-4bd4-467d-8034-530c44cd4442', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-12 11:26:30.867941+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ea9f9cb3-9dac-40b0-84ae-f7454ad20733', 'ChaLLengeR', 'rental:collection_meters', '2026-07-12 11:26:30.885599+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('73cb8ad9-0efe-45b6-ab23-881038abb3b9', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-12 11:26:31.107541+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bff800c8-fd59-4ed2-9707-a5b9961a34cd', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-12 11:26:33.407478+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d12babfe-9cce-4c1c-980f-cd33ae47c2df', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-12 11:26:33.933591+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0feb968c-67b8-409f-987e-3e9eda86de36', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-12 11:27:00.466228+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('2a3114e9-9455-4457-994f-8c8a0f8e0f57', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-12 11:23:34.598366+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('9e4a6c7e-6ab3-4512-8f02-7fe69391a6a1', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-12 11:23:35.269396+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('eca82200-0edc-4483-8f49-b79e5d910848', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-12 11:23:35.392054+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('11d3cf47-1c38-451a-8383-6a070cfafc5f', 'ChaLLengeR', 'rental:collection_tenants', '2026-07-12 11:24:23.596027+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4bd3c1a9-567e-4ac5-9e63-e961e74045de', 'ChaLLengeR', 'rental:collection_meters', '2026-07-12 11:24:23.612541+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ceca1f7b-a30d-4e1a-95ac-978534e24775', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-12 11:24:48.182285+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3aca5207-890a-4d90-a87a-f1ac63473637', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-12 11:26:29.363108+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1b59f173-6e44-4bc5-b3b8-e1ce393504d3', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-12 11:26:30.862891+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('ff4d2a50-aaf6-420f-b186-1ce2d7251de7', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-12 11:26:30.884901+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('4614cc75-9077-4844-9cfa-8195968bf51b', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-12 11:26:33.411246+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('21a1ea88-9113-466f-91ba-7660ebe26d35', 'ChaLLengeR', 'rental:collection_beneficiaries', '2026-07-12 11:26:33.921409+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('a0250dcb-965e-4962-a879-3e6bc411c97d', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-12 11:26:53.625008+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1d723661-a11c-426b-afb5-6a660edc1d5b', 'ChaLLengeR', 'rental:collection_beneficiary_settlements', '2026-07-12 11:23:35.25736+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('62262d2e-7e51-4b51-bcb2-12032f28bb0d', 'ChaLLengeR', 'rental:collection_meter_readings', '2026-07-12 11:24:15.116018+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('120182f6-6899-456f-82c7-7947e6988e54', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-12 11:24:23.588515+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('7484a30d-2f36-4c12-99d5-dd05cc5dad34', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-12 11:24:23.612266+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('1f8834d0-0f16-48ed-a637-b0a51a3e2471', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-12 11:24:23.762641+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('c330b582-0f40-4022-b46e-a69e96ff951c', 'ChaLLengeR', 'rental:preview_billing_period', '2026-07-12 11:24:55.509006+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('cc578eec-dd8c-4343-b101-20cacb768906', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-12 11:26:29.429313+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3536f33b-59e9-4a57-ae7e-46097868a67b', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-12 11:26:30.880956+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('e1093e6f-ed6f-45d9-9884-8670d9300bfb', 'ChaLLengeR', 'rental:collection_tenancies', '2026-07-12 11:26:31.012493+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('3694bd3c-36ac-40a4-b9de-ac078baa865d', 'ChaLLengeR', 'rental:collection_apartments', '2026-07-12 11:26:33.400604+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('bf4fedac-2c12-4c0c-b3f2-fe4ba34cab87', 'ChaLLengeR', 'rental:collection_apartment_costs', '2026-07-12 11:26:33.416283+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('d7a56ac9-88b9-4964-a196-676f47340b84', 'ChaLLengeR', 'rental:collection_cost_types', '2026-07-12 11:26:33.449371+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('b39d9df9-cd1c-4523-b675-40d09b527b06', 'ChaLLengeR', 'rental:collection_meters', '2026-07-12 11:26:33.552737+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('0b38dcb2-a11f-4044-a0e4-29ec3441b38e', 'ChaLLengeR', 'rental:collection_allocation_rules', '2026-07-12 11:26:33.933433+02');
INSERT INTO public.logs (id, username, description, date) VALUES ('263a3e2c-e3b6-4a8f-9814-70deec6aad57', 'ChaLLengeR', 'rental:collection_billing_periods', '2026-07-12 11:26:50.870337+02');


--
-- TOC entry 5104 (class 0 OID 336524)
-- Dependencies: 225
-- Data for Name: namesoverdue; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.namesoverdue (id, name) VALUES ('fa2b6794-24d9-4e34-b19d-1888615bd8eb', 'Mama');


--
-- TOC entry 5105 (class 0 OID 336532)
-- Dependencies: 226
-- Data for Name: outstandingmoney; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.outstandingmoney (id, amount, name, date, id_name) VALUES ('6b58e655-d010-4859-abff-2f63b25961a3', 100, 'test', '2026-07-11', 'fa2b6794-24d9-4e34-b19d-1888615bd8eb');


--
-- TOC entry 5106 (class 0 OID 336540)
-- Dependencies: 227
-- Data for Name: rentals_apartments; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_apartments (id, name, description, is_active, created_at, updated_at) VALUES ('c62da468-60b2-42a7-915c-cfe14783ce2c', 'Mieszkanie Dziadka', 'mieszkanie dziadka', true, '2026-07-11 13:45:31.686315+02', '2026-07-11 13:45:31.686315+02');
INSERT INTO public.rentals_apartments (id, name, description, is_active, created_at, updated_at) VALUES ('eaafb7c6-c5a3-424b-b841-c54479173e57', 'Mieszkanie Dobudówka', NULL, true, '2026-07-11 13:46:02.306159+02', '2026-07-11 13:46:02.306159+02');
INSERT INTO public.rentals_apartments (id, name, description, is_active, created_at, updated_at) VALUES ('6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'Mieszkanie stajnia', NULL, true, '2026-07-11 13:46:10.847409+02', '2026-07-11 13:46:10.847409+02');
INSERT INTO public.rentals_apartments (id, name, description, is_active, created_at, updated_at) VALUES ('2b2e4b09-66ce-45c8-9efe-be52e763f56d', 'Mieszkanie Góra', NULL, true, '2026-07-11 13:46:18.845477+02', '2026-07-11 13:46:18.845477+02');


--
-- TOC entry 5107 (class 0 OID 336554)
-- Dependencies: 228
-- Data for Name: rentals_beneficiaries; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_beneficiaries (id, name, is_active, created_at, updated_at) VALUES ('5a2ed080-3392-4b3a-bc5c-49d28dc49018', 'Ja', true, '2026-07-11 15:41:13.408963+02', '2026-07-11 15:41:13.408963+02');
INSERT INTO public.rentals_beneficiaries (id, name, is_active, created_at, updated_at) VALUES ('9134e8ab-c0e7-43e7-ac7d-5e2d608b11e3', 'Mama', true, '2026-07-11 15:41:16.907242+02', '2026-07-11 15:41:16.907242+02');
INSERT INTO public.rentals_beneficiaries (id, name, is_active, created_at, updated_at) VALUES ('aba80368-0a34-4084-8257-26c3b787df69', 'Tata', true, '2026-07-11 15:41:19.577181+02', '2026-07-11 15:41:19.577181+02');


--
-- TOC entry 5109 (class 0 OID 336582)
-- Dependencies: 230
-- Data for Name: rentals_cost_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_cost_types (id, name, charge_type, is_active, created_at, updated_at) VALUES ('ff10f25f-33cf-447d-965a-d6537b1ba33c', 'śmieci', 'per_person', true, '2026-07-11 13:53:14.894111+02', '2026-07-11 13:53:14.894111+02');
INSERT INTO public.rentals_cost_types (id, name, charge_type, is_active, created_at, updated_at) VALUES ('a89900fe-d7ea-498f-8142-b7b2c85d2a73', 'szambo', 'fixed', true, '2026-07-11 13:53:22.775805+02', '2026-07-11 13:53:22.775805+02');
INSERT INTO public.rentals_cost_types (id, name, charge_type, is_active, created_at, updated_at) VALUES ('57040cec-ee16-475d-8e2a-46b5defddc51', 'internet', 'fixed', true, '2026-07-11 13:53:29.81946+02', '2026-07-11 13:53:29.81946+02');


--
-- TOC entry 5113 (class 0 OID 336625)
-- Dependencies: 234
-- Data for Name: rentals_allocation_rules; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('5c7f901d-65f9-4681-9fa5-a3aa955d9189', 'aba80368-0a34-4084-8257-26c3b787df69', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'recurring', NULL, 'fixed_amount', 200.00, '2026-01-01', NULL, '2026-07-11 15:50:02.420268+02', '2026-07-11 15:50:02.420268+02', 'garaż');
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('d3e91067-8e1b-45ab-86f1-217deacded11', '9134e8ab-c0e7-43e7-ac7d-5e2d608b11e3', NULL, 'recurring', NULL, 'full', 360.00, '2026-01-01', NULL, '2026-07-11 15:52:07.583053+02', '2026-07-11 15:52:07.583053+02', 'podatek');
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('0b1c3701-8fab-46bd-8cfa-b469f81999ac', '9134e8ab-c0e7-43e7-ac7d-5e2d608b11e3', NULL, 'water', NULL, 'full', NULL, '2026-01-01', NULL, '2026-07-11 15:48:08.518885+02', '2026-07-11 15:52:35.307458+02', NULL);
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('1f5b337b-fc07-43c0-b3ae-62e53ea93028', '5a2ed080-3392-4b3a-bc5c-49d28dc49018', NULL, 'electricity', NULL, 'full', NULL, '2026-01-01', NULL, '2026-07-11 15:45:23.98699+02', '2026-07-11 15:52:58.026882+02', NULL);
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('e3dcb011-2601-4907-bc82-6f77f139b72b', '9134e8ab-c0e7-43e7-ac7d-5e2d608b11e3', NULL, 'cost_type', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 'full', NULL, '2026-01-01', NULL, '2026-07-11 16:21:28.802906+02', '2026-07-11 16:24:52.514155+02', 'smieci');
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('df4b1e15-4d2c-4d76-bfe7-06c727a1748f', '9134e8ab-c0e7-43e7-ac7d-5e2d608b11e3', NULL, 'cost_type', '57040cec-ee16-475d-8e2a-46b5defddc51', 'full', NULL, '2026-01-01', NULL, '2026-07-11 16:25:41.095009+02', '2026-07-11 16:25:41.095009+02', 'internet');
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('6a500df4-64b5-4b71-b900-9354ea128fd0', 'aba80368-0a34-4084-8257-26c3b787df69', 'eaafb7c6-c5a3-424b-b841-c54479173e57', 'rent', NULL, 'full', NULL, '2026-01-01', NULL, '2026-07-11 16:41:18.970275+02', '2026-07-11 16:41:18.970275+02', NULL);
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('ee18176a-dfa5-48d9-a3cd-e8d0955bc999', 'aba80368-0a34-4084-8257-26c3b787df69', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', 'rent', NULL, 'full', NULL, '2025-12-01', NULL, '2026-07-11 16:41:59.216107+02', '2026-07-11 16:41:59.216107+02', NULL);
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('9479489c-9af0-4c2f-9395-e1b44c157fc9', 'aba80368-0a34-4084-8257-26c3b787df69', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'rent', NULL, 'full', NULL, '2026-01-01', NULL, '2026-07-11 16:42:38.290764+02', '2026-07-11 16:42:38.290764+02', NULL);
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('f377a661-ebe7-4e61-ab03-ee5c3d219306', '5a2ed080-3392-4b3a-bc5c-49d28dc49018', 'c62da468-60b2-42a7-915c-cfe14783ce2c', 'rent', NULL, 'full', NULL, '2026-01-01', NULL, '2026-07-11 15:42:34.830319+02', '2026-07-11 16:42:53.575624+02', NULL);
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('660a7326-ab40-4856-84f9-9e3d052f8fe1', '5a2ed080-3392-4b3a-bc5c-49d28dc49018', 'c62da468-60b2-42a7-915c-cfe14783ce2c', 'recurring', NULL, 'fixed_amount', -90.00, '2026-01-01', NULL, '2026-07-11 16:58:52.842324+02', '2026-07-11 16:58:52.842324+02', 'podatek');
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('5a3bdf63-f357-4cb9-a278-791c234862e2', 'aba80368-0a34-4084-8257-26c3b787df69', 'eaafb7c6-c5a3-424b-b841-c54479173e57', 'recurring', NULL, 'fixed_amount', -90.00, '2026-01-01', NULL, '2026-07-11 16:59:20.414703+02', '2026-07-11 16:59:20.414703+02', 'podatek');
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('5cdd20b6-4871-450f-89de-65daedfee95f', 'aba80368-0a34-4084-8257-26c3b787df69', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', 'recurring', NULL, 'fixed_amount', -90.00, '2026-01-01', NULL, '2026-07-11 16:59:38.679331+02', '2026-07-11 16:59:38.679331+02', 'podatek');
INSERT INTO public.rentals_allocation_rules (id, beneficiary_id, apartment_id, component, cost_type_id, mode, amount, start_date, end_date, created_at, updated_at, description) VALUES ('31ec6680-e0b7-40ee-ba4d-ba268e60cab3', 'aba80368-0a34-4084-8257-26c3b787df69', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'recurring', NULL, 'full', -90.00, '2026-01-01', NULL, '2026-07-11 16:59:56.266298+02', '2026-07-11 16:59:56.266298+02', 'podatek');


--
-- TOC entry 5114 (class 0 OID 336654)
-- Dependencies: 235
-- Data for Name: rentals_apartment_costs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_apartment_costs (id, apartment_id, cost_type_id, amount, start_date, end_date, created_at, updated_at) VALUES ('e965717a-dd7a-4388-809e-35fbcc89e2b0', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', '57040cec-ee16-475d-8e2a-46b5defddc51', 60.00, '2026-01-01', NULL, '2026-07-11 13:57:03.431136+02', '2026-07-11 13:59:30.553249+02');
INSERT INTO public.rentals_apartment_costs (id, apartment_id, cost_type_id, amount, start_date, end_date, created_at, updated_at) VALUES ('2626cfc5-1fdf-4013-acdf-77264ba7e2e5', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 35.00, '2026-01-01', NULL, '2026-07-11 14:00:05.765057+02', '2026-07-11 14:00:05.765057+02');
INSERT INTO public.rentals_apartment_costs (id, apartment_id, cost_type_id, amount, start_date, end_date, created_at, updated_at) VALUES ('6eb6183f-2e9b-4a46-9572-bacd36ebfc47', 'c62da468-60b2-42a7-915c-cfe14783ce2c', '57040cec-ee16-475d-8e2a-46b5defddc51', 60.00, '2026-01-01', NULL, '2026-07-11 14:00:35.706348+02', '2026-07-11 14:00:35.706348+02');
INSERT INTO public.rentals_apartment_costs (id, apartment_id, cost_type_id, amount, start_date, end_date, created_at, updated_at) VALUES ('1f64ac6a-37d1-4fa6-a6b5-c807239d0d1d', 'c62da468-60b2-42a7-915c-cfe14783ce2c', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 35.00, '2026-01-01', NULL, '2026-07-11 14:01:15.062418+02', '2026-07-11 14:01:15.062418+02');
INSERT INTO public.rentals_apartment_costs (id, apartment_id, cost_type_id, amount, start_date, end_date, created_at, updated_at) VALUES ('5098e37f-4f17-4602-a97d-8f27401a3ead', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 35.00, '2026-01-01', NULL, '2026-07-11 14:01:55.094118+02', '2026-07-11 14:01:55.094118+02');
INSERT INTO public.rentals_apartment_costs (id, apartment_id, cost_type_id, amount, start_date, end_date, created_at, updated_at) VALUES ('659ea3f1-ed80-4444-b9cb-d9072922790b', 'eaafb7c6-c5a3-424b-b841-c54479173e57', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 35.00, '2026-01-01', NULL, '2026-07-11 14:03:01.761874+02', '2026-07-11 14:03:01.761874+02');


--
-- TOC entry 5108 (class 0 OID 336566)
-- Dependencies: 229
-- Data for Name: rentals_billing_periods; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_billing_periods (id, period_month, status, electricity_bill_amount, electricity_rate, electricity_rate_is_manual, water_rate, note, created_at, updated_at) VALUES ('78633a03-9586-4ec5-ac65-e34f44464b9f', '2026-06-01', 'closed', 492.94, 1.2139, false, 9.00, NULL, '2026-07-11 15:54:10.378014+02', '2026-07-11 17:02:18.608798+02');


--
-- TOC entry 5115 (class 0 OID 336678)
-- Dependencies: 236
-- Data for Name: rentals_beneficiary_settlements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_beneficiary_settlements (id, period_id, beneficiary_id, total_amount, created_at, updated_at) VALUES ('86b65959-295a-4970-bccb-1d51bd560def', '78633a03-9586-4ec5-ac65-e34f44464b9f', '5a2ed080-3392-4b3a-bc5c-49d28dc49018', 403.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlements (id, period_id, beneficiary_id, total_amount, created_at, updated_at) VALUES ('9263f459-64ce-4bb8-ad20-6cfcbec3c259', '78633a03-9586-4ec5-ac65-e34f44464b9f', '9134e8ab-c0e7-43e7-ac7d-5e2d608b11e3', 803.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlements (id, period_id, beneficiary_id, total_amount, created_at, updated_at) VALUES ('8f162f65-db71-44a8-be35-3491b42626af', '78633a03-9586-4ec5-ac65-e34f44464b9f', 'aba80368-0a34-4084-8257-26c3b787df69', 2930.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');


--
-- TOC entry 5110 (class 0 OID 336595)
-- Dependencies: 231
-- Data for Name: rentals_tenants; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_tenants (id, first_name, last_name, note, is_active, created_at, updated_at) VALUES ('787a89a3-659c-415f-9c29-a97616c9d49c', 'Łukasz', 'Kydr', NULL, true, '2026-07-11 13:46:40.646687+02', '2026-07-11 13:46:40.646687+02');
INSERT INTO public.rentals_tenants (id, first_name, last_name, note, is_active, created_at, updated_at) VALUES ('fe1db83b-3395-4c44-a276-1b0550d09de0', 'Witek', 'Naumuneko', NULL, true, '2026-07-11 13:46:48.794863+02', '2026-07-11 13:46:48.794863+02');
INSERT INTO public.rentals_tenants (id, first_name, last_name, note, is_active, created_at, updated_at) VALUES ('788d07b4-2ad3-43b9-841d-27519aa637d8', 'Ola', 'Dudzik', NULL, true, '2026-07-11 13:46:58.279469+02', '2026-07-11 13:46:58.279469+02');
INSERT INTO public.rentals_tenants (id, first_name, last_name, note, is_active, created_at, updated_at) VALUES ('d4f87fd1-e316-4cd4-9004-c8959ed1e0c1', 'Maciek', 'Dudzik', NULL, true, '2026-07-11 13:47:03.883535+02', '2026-07-11 13:47:03.883535+02');


--
-- TOC entry 5117 (class 0 OID 336720)
-- Dependencies: 238
-- Data for Name: rentals_tenancies; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_tenancies (id, apartment_id, tenant_id, rent_amount, persons_count, start_date, end_date, created_at, updated_at) VALUES ('8f40318e-7053-46eb-9f17-3cb67fbba7f7', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'fe1db83b-3395-4c44-a276-1b0550d09de0', 1000.00, 2, '2026-01-01', NULL, '2026-07-11 13:51:52.509844+02', '2026-07-11 16:32:02.093144+02');
INSERT INTO public.rentals_tenancies (id, apartment_id, tenant_id, rent_amount, persons_count, start_date, end_date, created_at, updated_at) VALUES ('bf39aacb-dc63-4473-bd41-65dbddfad952', 'eaafb7c6-c5a3-424b-b841-c54479173e57', '787a89a3-659c-415f-9c29-a97616c9d49c', 1000.00, 1, '2026-01-01', NULL, '2026-07-11 13:51:34.875441+02', '2026-07-11 16:32:23.499752+02');
INSERT INTO public.rentals_tenancies (id, apartment_id, tenant_id, rent_amount, persons_count, start_date, end_date, created_at, updated_at) VALUES ('1f63ee17-9de1-45d1-8705-2ca0b62375d8', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', '788d07b4-2ad3-43b9-841d-27519aa637d8', 1000.00, 2, '2026-01-01', NULL, '2026-07-11 13:51:14.484116+02', '2026-07-11 16:32:38.022892+02');


--
-- TOC entry 5119 (class 0 OID 336772)
-- Dependencies: 240
-- Data for Name: rentals_settlements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_settlements (id, period_id, apartment_id, tenancy_id, rent_amount, electricity_consumption, electricity_cost, water_consumption, water_cost, total_media_amount, total_amount, note, created_at, updated_at) VALUES ('bbfd8656-d4c6-4da5-a51a-3db1ef6f7f96', '78633a03-9586-4ec5-ac65-e34f44464b9f', 'eaafb7c6-c5a3-424b-b841-c54479173e57', 'bf39aacb-dc63-4473-bd41-65dbddfad952', 1000.00, 54.890, 67.00, 0.652, 6.00, 108.00, 1108.00, NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlements (id, period_id, apartment_id, tenancy_id, rent_amount, electricity_consumption, electricity_cost, water_consumption, water_cost, total_media_amount, total_amount, note, created_at, updated_at) VALUES ('114f458a-d5db-492e-8e83-cc38e73a1718', '78633a03-9586-4ec5-ac65-e34f44464b9f', 'c62da468-60b2-42a7-915c-cfe14783ce2c', NULL, 0.00, 0.000, 0.00, 0.019, 0.00, 95.00, 95.00, NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlements (id, period_id, apartment_id, tenancy_id, rent_amount, electricity_consumption, electricity_cost, water_consumption, water_cost, total_media_amount, total_amount, note, created_at, updated_at) VALUES ('b381f0d5-721d-4859-83cc-b655e4580c3d', '78633a03-9586-4ec5-ac65-e34f44464b9f', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', '1f63ee17-9de1-45d1-8705-2ca0b62375d8', 1000.00, 221.750, 269.00, 6.222, 56.00, 455.00, 1455.00, NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlements (id, period_id, apartment_id, tenancy_id, rent_amount, electricity_consumption, electricity_cost, water_consumption, water_cost, total_media_amount, total_amount, note, created_at, updated_at) VALUES ('8c7fd004-4c2f-4190-8f56-47c5806d0292', '78633a03-9586-4ec5-ac65-e34f44464b9f', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', '8f40318e-7053-46eb-9f17-3cb67fbba7f7', 1000.00, 129.450, 157.00, 5.659, 51.00, 278.00, 1278.00, NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');


--
-- TOC entry 5120 (class 0 OID 336810)
-- Dependencies: 241
-- Data for Name: rentals_beneficiary_settlement_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('0f5bd47f-c4a8-450b-9013-21a9caeacbd4', '86b65959-295a-4970-bccb-1d51bd560def', 'czynsz - Mieszkanie Dziadka', 0.00, 'f377a661-ebe7-4e61-ab03-ee5c3d219306', '114f458a-d5db-492e-8e83-cc38e73a1718', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('53d888ae-16c2-4482-b1b3-00eee11603fc', '86b65959-295a-4970-bccb-1d51bd560def', 'prąd - Mieszkanie Dobudówka', 67.00, '1f5b337b-fc07-43c0-b3ae-62e53ea93028', 'bbfd8656-d4c6-4da5-a51a-3db1ef6f7f96', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('1a3e3ed3-b4a6-4d7e-8f46-5d27bdbb097e', '86b65959-295a-4970-bccb-1d51bd560def', 'prąd - Mieszkanie Dziadka', 0.00, '1f5b337b-fc07-43c0-b3ae-62e53ea93028', '114f458a-d5db-492e-8e83-cc38e73a1718', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('3e08080c-2c59-4208-b324-0b7c333b3bdf', '86b65959-295a-4970-bccb-1d51bd560def', 'prąd - Mieszkanie Góra', 269.00, '1f5b337b-fc07-43c0-b3ae-62e53ea93028', 'b381f0d5-721d-4859-83cc-b655e4580c3d', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('c77490c3-c7c1-4e6c-a02a-162147d22edb', '86b65959-295a-4970-bccb-1d51bd560def', 'prąd - Mieszkanie stajnia', 157.00, '1f5b337b-fc07-43c0-b3ae-62e53ea93028', '8c7fd004-4c2f-4190-8f56-47c5806d0292', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('27ac4bd6-d010-430c-baa3-7061d5ea95d3', '86b65959-295a-4970-bccb-1d51bd560def', 'podatek', -90.00, '660a7326-ab40-4856-84f9-9e3d052f8fe1', NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('27cbe332-544f-4482-b6f1-3cec035182b7', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'woda - Mieszkanie Dobudówka', 6.00, '0b1c3701-8fab-46bd-8cfa-b469f81999ac', 'bbfd8656-d4c6-4da5-a51a-3db1ef6f7f96', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('69ce6c51-e33d-4c0d-85b8-197b3ced7cd7', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'woda - Mieszkanie Dziadka', 0.00, '0b1c3701-8fab-46bd-8cfa-b469f81999ac', '114f458a-d5db-492e-8e83-cc38e73a1718', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('135e41c5-2c38-4124-ae05-911f6e4fadf1', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'woda - Mieszkanie Góra', 56.00, '0b1c3701-8fab-46bd-8cfa-b469f81999ac', 'b381f0d5-721d-4859-83cc-b655e4580c3d', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('4f1e4b07-9b75-4bd9-b0dd-5cd97b9bf4fb', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'woda - Mieszkanie stajnia', 51.00, '0b1c3701-8fab-46bd-8cfa-b469f81999ac', '8c7fd004-4c2f-4190-8f56-47c5806d0292', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('29fef5a3-73c8-42af-af39-12b28afee3a7', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'podatek', 360.00, 'd3e91067-8e1b-45ab-86f1-217deacded11', NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('cb34cd7f-95d7-4955-9da3-94390a6a59c9', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'smieci - Mieszkanie Dobudówka', 35.00, 'e3dcb011-2601-4907-bc82-6f77f139b72b', 'bbfd8656-d4c6-4da5-a51a-3db1ef6f7f96', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('1901fc20-6566-46e9-9d0d-c607e97c2cc2', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'smieci - Mieszkanie Dziadka', 35.00, 'e3dcb011-2601-4907-bc82-6f77f139b72b', '114f458a-d5db-492e-8e83-cc38e73a1718', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('ac45f5dd-4c04-47f8-a1f7-cb3441985884', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'smieci - Mieszkanie Góra', 70.00, 'e3dcb011-2601-4907-bc82-6f77f139b72b', 'b381f0d5-721d-4859-83cc-b655e4580c3d', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('32643322-53b3-4b94-9959-f07c4162a575', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'smieci - Mieszkanie stajnia', 70.00, 'e3dcb011-2601-4907-bc82-6f77f139b72b', '8c7fd004-4c2f-4190-8f56-47c5806d0292', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('c8bc8a4c-3cf8-42a8-a79e-8781cf2f7788', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'internet - Mieszkanie Dobudówka', 0.00, 'df4b1e15-4d2c-4d76-bfe7-06c727a1748f', 'bbfd8656-d4c6-4da5-a51a-3db1ef6f7f96', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('bec5a724-28ad-4c0e-b047-7ddbdbf5ecf0', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'internet - Mieszkanie Dziadka', 60.00, 'df4b1e15-4d2c-4d76-bfe7-06c727a1748f', '114f458a-d5db-492e-8e83-cc38e73a1718', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('57646732-a708-41e0-af6b-338f3c7f639d', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'internet - Mieszkanie Góra', 60.00, 'df4b1e15-4d2c-4d76-bfe7-06c727a1748f', 'b381f0d5-721d-4859-83cc-b655e4580c3d', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('d31a936e-704b-41bc-ba15-f00690947f3d', '9263f459-64ce-4bb8-ad20-6cfcbec3c259', 'internet - Mieszkanie stajnia', 0.00, 'df4b1e15-4d2c-4d76-bfe7-06c727a1748f', '8c7fd004-4c2f-4190-8f56-47c5806d0292', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('0e827d3f-d394-4710-a471-30635ba82382', '8f162f65-db71-44a8-be35-3491b42626af', 'garaż', 200.00, '5c7f901d-65f9-4681-9fa5-a3aa955d9189', NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('b0f0145c-7c38-4a49-830b-61d2e2b1bde6', '8f162f65-db71-44a8-be35-3491b42626af', 'czynsz - Mieszkanie Dobudówka', 1000.00, '6a500df4-64b5-4b71-b900-9354ea128fd0', 'bbfd8656-d4c6-4da5-a51a-3db1ef6f7f96', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('c14fe350-afe1-422b-a5f7-e017999000c9', '8f162f65-db71-44a8-be35-3491b42626af', 'czynsz - Mieszkanie Góra', 1000.00, 'ee18176a-dfa5-48d9-a3cd-e8d0955bc999', 'b381f0d5-721d-4859-83cc-b655e4580c3d', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('beb7ab13-1e73-4900-a5d6-85778157ff31', '8f162f65-db71-44a8-be35-3491b42626af', 'czynsz - Mieszkanie stajnia', 1000.00, '9479489c-9af0-4c2f-9395-e1b44c157fc9', '8c7fd004-4c2f-4190-8f56-47c5806d0292', '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('a543f40a-d5a7-4417-b975-b6acf261916e', '8f162f65-db71-44a8-be35-3491b42626af', 'podatek', -90.00, '5a3bdf63-f357-4cb9-a278-791c234862e2', NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('d21462fb-7bb2-4b8a-bbef-cebd676eccb2', '8f162f65-db71-44a8-be35-3491b42626af', 'podatek', -90.00, '5cdd20b6-4871-450f-89de-65daedfee95f', NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_beneficiary_settlement_items (id, beneficiary_settlement_id, description, amount, rule_id, settlement_id, created_at, updated_at) VALUES ('1d6ab5ef-1207-4ae0-9743-8b182e40a367', '8f162f65-db71-44a8-be35-3491b42626af', 'podatek', -90.00, '31ec6680-e0b7-40ee-ba4d-ba268e60cab3', NULL, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');


--
-- TOC entry 5116 (class 0 OID 336703)
-- Dependencies: 237
-- Data for Name: rentals_meters; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('7b0f44a9-350c-4bc4-80cf-64052bbedc25', 'c62da468-60b2-42a7-915c-cfe14783ce2c', 'electricity', false, NULL, true, '2026-07-11 14:09:59.190416+02', '2026-07-11 14:09:59.190416+02');
INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('3a966aa2-edb0-4ea5-9e26-d7346f826d6a', 'c62da468-60b2-42a7-915c-cfe14783ce2c', 'water', true, NULL, true, '2026-07-11 14:10:15.297325+02', '2026-07-11 14:10:15.297325+02');
INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('7ea6286f-998e-4b4e-a811-7e348baae0bc', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', 'electricity', false, NULL, true, '2026-07-11 14:10:21.39984+02', '2026-07-11 14:10:21.39984+02');
INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('3018fb9e-5adb-4511-b308-535a0a97bf69', '2b2e4b09-66ce-45c8-9efe-be52e763f56d', 'water', false, NULL, true, '2026-07-11 14:10:27.439274+02', '2026-07-11 14:10:27.439274+02');
INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('62a8d36c-9c68-4b11-b2bb-b3a2e6001090', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'electricity', false, NULL, true, '2026-07-11 14:10:33.998993+02', '2026-07-11 14:10:33.998993+02');
INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('560e0a3e-d783-48c0-a4e9-c28bba1b3d6f', '6a1f69f7-a5d9-4524-ab4d-4ade410f723e', 'water', false, NULL, true, '2026-07-11 14:10:39.724246+02', '2026-07-11 14:10:39.724246+02');
INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('0733fe75-dbb4-4c1c-97fe-849c50c873c2', 'eaafb7c6-c5a3-424b-b841-c54479173e57', 'electricity', false, NULL, true, '2026-07-11 14:11:47.921206+02', '2026-07-11 14:11:47.921206+02');
INSERT INTO public.rentals_meters (id, apartment_id, media_type, is_master, name, is_active, created_at, updated_at) VALUES ('70f76d37-324f-439d-bd13-cbed71ea2bf5', 'eaafb7c6-c5a3-424b-b841-c54479173e57', 'water', false, NULL, true, '2026-07-11 14:11:54.241003+02', '2026-07-11 14:11:54.241003+02');


--
-- TOC entry 5118 (class 0 OID 336745)
-- Dependencies: 239
-- Data for Name: rentals_meter_readings; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('8556f466-a97c-4b35-a01e-515813245b7a', '78633a03-9586-4ec5-ac65-e34f44464b9f', '7ea6286f-998e-4b4e-a811-7e348baae0bc', 10403.190, 10624.940, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 15:55:33.927415+02');
INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('a09cf8bd-977c-416e-b313-7bd84183f4d6', '78633a03-9586-4ec5-ac65-e34f44464b9f', '3018fb9e-5adb-4511-b308-535a0a97bf69', 240.674, 246.896, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 15:56:21.570742+02');
INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('fea8cca9-2130-444d-938a-d47cd547cc33', '78633a03-9586-4ec5-ac65-e34f44464b9f', '0733fe75-dbb4-4c1c-97fe-849c50c873c2', 6453.310, 6508.200, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 15:56:40.413683+02');
INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('c1c3ae7c-9cab-4a2f-8e54-e0c5c0a2c808', '78633a03-9586-4ec5-ac65-e34f44464b9f', '70f76d37-324f-439d-bd13-cbed71ea2bf5', 94.984, 95.636, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 15:56:50.981418+02');
INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('6269da97-1f0e-4548-a1eb-d54185df4847', '78633a03-9586-4ec5-ac65-e34f44464b9f', '560e0a3e-d783-48c0-a4e9-c28bba1b3d6f', 146.440, 152.099, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 15:57:17.980712+02');
INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('91fca711-63a7-4c92-8912-e90d47d925c5', '78633a03-9586-4ec5-ac65-e34f44464b9f', '7b0f44a9-350c-4bc4-80cf-64052bbedc25', 8217.470, 8217.470, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 15:59:14.086081+02');
INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('fa2764a6-9bf8-4e91-a92e-e143742081bb', '78633a03-9586-4ec5-ac65-e34f44464b9f', '62a8d36c-9c68-4b11-b2bb-b3a2e6001090', 5195.090, 5324.540, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 16:10:43.597372+02');
INSERT INTO public.rentals_meter_readings (id, period_id, meter_id, previous_value, current_value, error_correction, created_at, updated_at) VALUES ('bf8c9a58-eb95-4d4e-8264-ce4b5c501737', '78633a03-9586-4ec5-ac65-e34f44464b9f', '3a966aa2-edb0-4ea5-9e26-d7346f826d6a', 727.048, 739.600, 0.000, '2026-07-11 15:54:10.378014+02', '2026-07-11 16:23:46.395098+02');


--
-- TOC entry 5121 (class 0 OID 336837)
-- Dependencies: 242
-- Data for Name: rentals_settlement_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rentals_settlement_items (id, settlement_id, cost_type_id, name, kind, amount, created_at, updated_at) VALUES ('e286ba36-61e8-49e5-b384-2a9198ad9988', 'bbfd8656-d4c6-4da5-a51a-3db1ef6f7f96', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 'śmieci (1 os. x 35.0 zł)', 'fixed_cost', 35.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlement_items (id, settlement_id, cost_type_id, name, kind, amount, created_at, updated_at) VALUES ('c797044c-03ad-402f-adc7-8bbfceabdd1d', '114f458a-d5db-492e-8e83-cc38e73a1718', '57040cec-ee16-475d-8e2a-46b5defddc51', 'internet', 'fixed_cost', 60.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlement_items (id, settlement_id, cost_type_id, name, kind, amount, created_at, updated_at) VALUES ('e7cf6ec2-3c9b-4375-950c-6544f43cdfc9', '114f458a-d5db-492e-8e83-cc38e73a1718', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 'śmieci (1 os. x 35.0 zł)', 'fixed_cost', 35.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlement_items (id, settlement_id, cost_type_id, name, kind, amount, created_at, updated_at) VALUES ('e976bea3-fd7d-42e4-9579-e7427cbdf42f', 'b381f0d5-721d-4859-83cc-b655e4580c3d', '57040cec-ee16-475d-8e2a-46b5defddc51', 'internet', 'fixed_cost', 60.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlement_items (id, settlement_id, cost_type_id, name, kind, amount, created_at, updated_at) VALUES ('4782524c-a00b-401e-81e7-6cbceca682e9', 'b381f0d5-721d-4859-83cc-b655e4580c3d', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 'śmieci (2 os. x 35.0 zł)', 'fixed_cost', 70.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');
INSERT INTO public.rentals_settlement_items (id, settlement_id, cost_type_id, name, kind, amount, created_at, updated_at) VALUES ('eb89c580-9b3f-4085-a968-244a8ece5aa1', '8c7fd004-4c2f-4190-8f56-47c5806d0292', 'ff10f25f-33cf-447d-965a-d6537b1ba33c', 'śmieci (2 os. x 35.0 zł)', 'fixed_cost', 70.00, '2026-07-11 17:02:18.608798+02', '2026-07-11 17:02:18.608798+02');


--
-- TOC entry 5111 (class 0 OID 336607)
-- Dependencies: 232
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5112 (class 0 OID 336617)
-- Dependencies: 233
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (id, username, password, type) VALUES ('95e17740-3150-4cdf-9199-0bb3e4c31dc0', 'yoho', '$2a$10$37XTsu9V5Dg972oJlkMJHuHTBAWUFJk5K7m8mRbCtGSGnE8WyCEiO', 'admin');
INSERT INTO public.users (id, username, password, type) VALUES ('ed2f5efd-3320-4576-9e1c-7dee45f800e4', 'ChaLLengeR', '$2a$10$Hy0jE4pS1pE5RJKlcBtxn.ndyw7LTuIvptACb1Ft5gQAjDHltHLSi', 'superadmin');


-- Completed on 2026-07-12 18:42:38

--
-- PostgreSQL database dump complete
--

\unrestrict fcfyriaEfvT6IWewQYVEQCShkH87nCcvpVgbB7FaAaVqvy4izFzpKijtBfkC0nC

