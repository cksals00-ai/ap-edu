# -*- coding: utf-8 -*-
"""30일 챌린지 — 베트남어·프랑스어 페이지 (앱 힌트 언어와 같음). 체험단·게시판·나머지 페이지는 한/영만 있어 영어로 연결."""
from content import CHALLENGE as C

dm = lambda d: f'{int(d[8:])}/{int(d[5:7])}'
a0, a1 = C['apply']; r0, r1 = C['run']
AGES = ['', '4–6', '7–9', '10–12', '13+']
DEV = lambda both: [('iphone', 'iPhone'), ('ipad', 'iPad'), ('both', both)]

# 셸(머리글·바닥글)용 — 메뉴는 영어 페이지로 연결
T_EXTRA = {
 'vi': dict(lang='vi', other='en', otherLabel='EN',
   nav=[('/en/', 'Trang chủ'), ('/en/cubs/', 'Bốn chú hổ'), ('/en/episodes/', 'Tập phim'), ('/en/app/', 'Ứng dụng'), ('/vi/event/challenge/', 'Sự kiện'), ('/en/board/', 'Bảng tin'), ('/en/news/', 'Tin tức')],
   store='App Store', ytch='Kênh YouTube', privacy='Chính sách quyền riêng tư', company='Công ty',
   studio='AP Edu là thương hiệu giáo dục của A.P Holdings.', footer_note='Hangeul Cubs © 2026 AP Edu / A.P Holdings. Nhân vật, hình ảnh và nội dung thuộc về AP Edu. Hình minh họa được tạo bằng công cụ AI.'),
 'fr': dict(lang='fr', other='en', otherLabel='EN',
   nav=[('/en/', 'Accueil'), ('/en/cubs/', 'Les tigres'), ('/en/episodes/', 'Épisodes'), ('/en/app/', 'L’app'), ('/fr/event/challenge/', 'Événements'), ('/en/board/', 'Forum'), ('/en/news/', 'Actus')],
   store='App Store', ytch='Chaîne YouTube', privacy='Confidentialité', company='Société',
   studio='AP Edu est le label éducatif d’A.P Holdings.', footer_note='Hangeul Cubs © 2026 AP Edu / A.P Holdings. Personnages, illustrations et contenus appartiennent à AP Edu. Illustrations réalisées avec des outils d’IA.'),
}

CH_I18N = {
 'vi': dict(
  title='30 ngày học tiếng Hàn cùng bốn chú hổ con. Một người nhận kính Meta AI.',
  lead='Học bằng ứng dụng và video suốt tháng 11, đăng cảm nhận lên bảng tin của chúng tôi và trang mạng xã hội của bạn — chúng tôi sẽ chấm chọn một người để tặng kính Ray-Ban Meta AI. Mọi quốc gia đều có thể tham gia.',
  steps=[('Đăng ký', f'{dm(a0)} – {dm(a1)}', 'Điền mẫu bên dưới. Từ 14 tuổi đăng ký bằng tên mình; phụ huynh đăng ký thay cho con.'),
         ('Thử thách', f'{dm(r0)} – {dm(r1)}', '30 ngày. Mỗi tuần một bài trên bảng tin.'),
         ('Hạn nộp cảm nhận', dm(C['review_due']), 'Cảm nhận trên bảng tin và bài đăng trên trang của bạn — cả hai.'),
         ('Công bố', dm(C['announce']), '1 giải nhất + 5 giải khuyến khích. Gửi quà trong tháng 12.')],
  do=[('4 bài nhật ký hằng tuần', 'Trên bảng tin, gắn thẻ #challenge W1–W4: một chữ bạn đã học, ảnh chụp tab Ôn tập trong ứng dụng, một dòng cảm nghĩ.'),
      ('Xem từ 3 tập', 'Ba trong số Bài học YouTube 1–5. Một dòng bình luận là đủ để xác nhận.'),
      ('Cảm nhận cuối — bảng tin', 'Từ 300 ký tự hoặc video từ 60 giây. Viết bằng ngôn ngữ nào cũng được.'),
      ('Cảm nhận cuối — trang của bạn', 'Bài đăng công khai trên blog, Instagram, TikTok, YouTube hoặc Facebook, gắn thẻ #HangeulCubs, rồi dán link vào bài cảm nhận trên bảng tin.')],
  score=[('40', 'Đều đặn', '4 bài nhật ký · tiến độ trong ứng dụng'), ('40', 'Nội dung', 'chữ nào, cảnh nào đã giúp bạn, điều gì nên sửa'), ('20', 'Cách thể hiện', 'video, tranh vẽ, sự tham gia của con bạn')],
  prize=[('Kính Ray-Ban Meta AI · 1 người', 'Khoảng 690.000 won theo giá bán lẻ tại Hàn Quốc. Đặt tại cửa hàng chính hãng ở quốc gia của người thắng. Nếu nơi đó chưa bán, thay bằng thẻ quà tặng Amazon hoặc Apple cùng giá trị (khoảng 450 USD).'),
         ('Khuyến khích · 5 người', 'Thẻ quà tặng App Store 30.000 won — hạng 6 đến 10.'),
         ('Thuế và vận chuyển', 'AP Edu chi trả thuế giải thưởng tại Hàn Quốc và phí gửi quà. Họ tên, địa chỉ và số điện thoại chỉ được hỏi riêng người thắng giải.')],
  rules=['Đơn vị tổ chức: AP Edu (A.P Holdings, Hàn Quốc). Meta, Ray-Ban, YouTube, Instagram và TikTok không phải nhà tài trợ và không chịu trách nhiệm gì về sự kiện này.',
         'Tham gia miễn phí, không cần mua hàng. Việc mua gói Batchim Master không ảnh hưởng đến việc chấm điểm.',
         'Từ 14 tuổi trở lên đăng ký bằng tên mình. Trẻ dưới 14 tuổi do phụ huynh đăng ký và tham gia dưới tên phụ huynh.',
         'Không áp dụng ở nơi pháp luật cấm, và cho cư dân Brazil, Ý, Quebec (Canada) do yêu cầu đăng ký trước tại địa phương.',
         'AP Edu chấm theo các tiêu chí trên; nếu bằng điểm, ưu tiên người nộp nhật ký tuần sớm hơn. Luôn chọn 1 người dù số người tham gia là bao nhiêu.',
         'Đánh giá hay xếp hạng trên App Store là tùy ý, không phải điều kiện. Thích hay đăng ký kênh cũng không phải điều kiện.',
         'Bài cảm nhận là của bạn. Chúng tôi có thể trích dẫn, chia sẻ để giới thiệu sự kiện và kênh (bạn đồng ý khi đăng ký).',
         'Thông tin cá nhân (tên, email, quốc gia, nhóm tuổi, thiết bị) chỉ dùng để vận hành sự kiện và được xóa sau đó. Thông tin giao hàng chỉ hỏi người thắng giải.',
         'Nhật ký giả, bài sao chép hoặc dùng nhiều tài khoản sẽ bị loại. Giải thưởng có thể được thay bằng sản phẩm cùng giá trị khi cần. AP Edu có quyền giải thích cuối cùng về thể lệ.',
         'Thuế giải thưởng tại Hàn Quốc (khấu trừ 22%) do AP Edu chi trả. Nếu quốc gia của bạn có thủ tục thuế hay nhập khẩu riêng, chúng tôi sẽ hướng dẫn.'],
  form_note=f'Đăng ký mở từ ngày {dm(a0)}. Trong lúc chờ, bạn có thể xem các bài học trên YouTube.', soon=f'Mở ngày {dm(a0)}',
  fx=dict(name='Tên hoặc biệt danh', email='Email', learner='Ai là người học?', learners=[('child', 'Trẻ em (phụ huynh đăng ký)'), ('adult', 'Người lớn · tôi'), ('family', 'Cả gia đình'), ('teacher', 'Giáo viên · lớp học')],
          age='Nhóm tuổi của trẻ (tùy chọn)', ages=AGES, country='Quốc gia · khu vực', device='Thiết bị', devices=DEV('Cả hai'),
          channel='Blog hoặc trang mạng xã hội nơi bạn sẽ đăng cảm nhận', note='Một dòng (tùy chọn — vì sao bạn học tiếng Hàn?)',
          consent='Tôi đã đọc thể lệ và đồng ý để thông tin của mình chỉ được dùng cho sự kiện, và bài cảm nhận có thể được trích dẫn.',
          submit='Đăng ký thử thách', ok='Đã nhận! Chúng tôi sẽ gửi email hướng dẫn vào ngày 1/11.', err='Chưa gửi được. Vui lòng thử lại sau ít phút.', many='Email này đã đăng ký rồi.'),
  h=dict(eyebrow='Thử thách 30 ngày · Tháng 11', do='Cần làm gì', doNote='Cần có cả cảm nhận trên bảng tin và bài đăng trên trang của bạn mới được chấm.', score='Chấm điểm · 100 điểm', scoreNote='Chấm điểm, không bốc thăm. Chỉ ba tiêu chí này.',
         prize='Giải thưởng', rules='Thể lệ chính thức', apply='Đăng ký', tester='Thử nghiệm · Tháng 10 (EN)', ch='Thử thách 30 ngày · Tháng 11', page='Thử thách 30 ngày — Kính Meta AI | Hangeul Cubs')),
 'fr': dict(
  title='30 jours de coréen avec les bébés tigres. Des lunettes Meta AI à gagner.',
  lead='Apprenez avec l’app et les vidéos tout au long de novembre, publiez votre avis sur notre forum et sur votre propre réseau social — un participant, choisi par un jury, recevra des lunettes Ray-Ban Meta AI. Ouvert à tous les pays.',
  steps=[('Inscription', f'{dm(a0)} – {dm(a1)}', 'Formulaire ci-dessous. Dès 14 ans en votre nom ; un parent inscrit son enfant.'),
         ('Défi', f'{dm(r0)} – {dm(r1)}', '30 jours. Un message par semaine sur le forum.'),
         ('Avis à rendre', dm(C['review_due']), 'Avis sur le forum et publication sur votre réseau — les deux.'),
         ('Résultats', dm(C['announce']), '1 gagnant + 5 prix d’encouragement. Envoi en décembre.')],
  do=[('4 journaux hebdomadaires', 'Sur le forum, avec le tag #challenge W1–W4 : une lettre apprise, une capture de l’onglet Révision de l’app, une phrase.'),
      ('3 épisodes ou plus', 'Trois des leçons YouTube 1 à 5. Un commentaire d’une ligne suffit à le montrer.'),
      ('Avis final — forum', '300 caractères minimum ou une vidéo de 60 secondes. Dans la langue de votre choix.'),
      ('Avis final — votre réseau', 'Une publication publique sur votre blog, Instagram, TikTok, YouTube ou Facebook avec #HangeulCubs, et le lien ajouté à votre avis sur le forum.')],
  score=[('40', 'Régularité', '4 journaux · progression dans l’app'), ('40', 'Contenu', 'quelles lettres, quelles scènes vous ont aidé, ce qu’il faut améliorer'), ('20', 'Expression', 'vidéo, dessins, participation de votre enfant')],
  prize=[('Lunettes Ray-Ban Meta AI · 1 gagnant', 'Environ 690 000 wons au prix public coréen. Commandées dans la boutique officielle du pays du gagnant. Là où elles ne sont pas vendues, une carte cadeau Amazon ou Apple de même valeur (environ 450 USD).'),
         ('Encouragement · 5', 'Carte cadeau App Store de 30 000 wons — places 6 à 10.'),
         ('Taxes et livraison', 'AP Edu prend en charge la taxe coréenne sur le lot et la livraison. Nom, adresse et téléphone ne sont demandés qu’au gagnant.')],
  rules=['Organisateur : AP Edu (A.P Holdings, République de Corée). Meta, Ray-Ban, YouTube, Instagram et TikTok ne sont pas partenaires de ce jeu et n’en portent aucune responsabilité.',
         'Participation gratuite et sans obligation d’achat. Acheter Batchim Master n’a aucun effet sur l’évaluation.',
         'Dès 14 ans, inscription en votre nom. Pour un enfant de moins de 14 ans, un parent s’inscrit et participe en son propre nom.',
         'Non ouvert là où la loi l’interdit, ni aux résidents du Brésil, d’Italie ou du Québec (formalités locales préalables).',
         'Le jury d’AP Edu évalue selon les critères ci-dessus ; en cas d’égalité, priorité aux journaux publiés le plus tôt. Un gagnant est désigné quel que soit le nombre de participants.',
         'Les notes et avis sur l’App Store sont libres et ne sont jamais une condition. Les « j’aime » et abonnements non plus.',
         'Votre avis vous appartient. Nous pouvons le citer ou le partager pour présenter le jeu et la chaîne (accord donné à l’inscription).',
         'Les données personnelles (nom, e-mail, pays, tranche d’âge, appareil) servent uniquement à l’organisation et sont supprimées ensuite. Les coordonnées de livraison ne sont demandées qu’au gagnant.',
         'Faux journaux, textes copiés ou comptes multiples entraînent l’exclusion. Le lot peut être remplacé par un lot de valeur équivalente si nécessaire. L’interprétation du règlement par AP Edu est définitive.',
         'La taxe coréenne sur le lot (retenue de 22 %) est payée par AP Edu. Si votre pays prévoit ses propres démarches fiscales ou douanières, nous vous accompagnons.'],
  form_note=f'Les inscriptions ouvrent le {dm(a0)}. En attendant, regardez les leçons sur YouTube.', soon=f'Ouverture le {dm(a0)}',
  fx=dict(name='Nom ou pseudo', email='E-mail', learner='Qui apprend ?', learners=[('child', 'Un enfant (inscrit par un parent)'), ('adult', 'Un adulte · moi'), ('family', 'Toute la famille'), ('teacher', 'Un enseignant · une classe')],
          age='Tranche d’âge de l’enfant (facultatif)', ages=AGES, country='Pays · région', device='Appareil', devices=DEV('Les deux'),
          channel='Votre blog ou réseau social où l’avis sera publié', note='Un mot (facultatif — pourquoi le coréen ?)',
          consent='J’ai lu le règlement et j’accepte que mes données servent uniquement à l’organisation du jeu et que mon avis puisse être cité.',
          submit='S’inscrire au défi', ok='C’est noté ! Nous vous écrirons le 1er novembre pour le lancement.', err='Envoi impossible. Réessayez dans un instant.', many='Cet e-mail est déjà inscrit.'),
  h=dict(eyebrow='Défi 30 jours · Novembre', do='À faire', doNote='L’avis sur le forum et la publication sur votre réseau sont tous deux requis pour être évalué.', score='Évaluation · 100 points', scoreNote='Sur jury, pas par tirage au sort. Ces trois critères seulement.',
         prize='Lots', rules='Règlement officiel', apply='Inscription', tester='Testeurs · Octobre (EN)', ch='Défi 30 jours · Novembre', page='Défi 30 jours — Lunettes Meta AI | Hangeul Cubs')),
}
