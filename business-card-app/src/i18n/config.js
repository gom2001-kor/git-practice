import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Translation resources
const resources = {
  ko: {
    translation: {
      // Common
      app_name: '디지털 명함',
      save: '저장',
      cancel: '취소',
      delete: '삭제',
      edit: '수정',
      add: '추가',
      remove: '제거',
      search: '검색',
      back: '뒤로',
      next: '다음',
      done: '완료',

      // Navigation
      my_cards: '내 명함',
      card_collection: '명함첩',
      settings: '설정',

      // Card Creation
      create_card: '명함 만들기',
      edit_card: '명함 수정',
      card_info: '명함 정보',
      name: '이름',
      photo: '사진',
      address: '주소',
      select_photo: '사진 선택',
      take_photo: '사진 촬영',
      from_gallery: '갤러리에서 선택',

      // Dynamic Fields
      phone: '전화번호',
      email: '이메일',
      website: '웹사이트',
      fax: 'FAX',
      add_phone: '전화번호 추가',
      add_email: '이메일 추가',
      add_website: '웹사이트 추가',
      add_fax: 'FAX 추가',
      label: '라벨',
      value: '값',

      // Field Labels
      office: '회사',
      personal: '개인',
      mobile: '휴대폰',
      work: '업무',
      home: '자택',
      main: '본사',
      branch: '지사',

      // Templates
      select_template: '템플릿 선택',
      template: '템플릿',

      // Themes
      select_theme: '테마 선택',
      blue_theme: '파란색 테마',
      pink_theme: '핑크색 테마',

      // Privacy
      privacy_setting: '공개 설정',
      public: '전체 공개',
      link_only: '링크를 아는 사람만',
      private: '비공개',

      // Share & QR
      share_card: '명함 공유',
      qr_code: 'QR 코드',
      scan_qr: 'QR 스캔',
      download_qr: 'QR 코드 다운로드',

      // Account
      account: '계정',
      link_account: '계정 연동',
      link_google: '구글 계정 연동',
      link_apple: '애플 계정 연동',
      anonymous_user: '익명 사용자',
      linked_account: '연동된 계정',

      // Messages
      copied: '복사되었습니다',
      email_copied: '이메일 주소가 복사되었습니다',
      fax_copied: 'FAX 번호가 복사되었습니다',
      card_saved: '명함이 저장되었습니다',
      card_deleted: '명함이 삭제되었습니다',
      max_fields: '최대 3개까지 추가할 수 있습니다',

      // Errors
      error: '오류',
      error_loading: '로딩 중 오류가 발생했습니다',
      error_saving: '저장 중 오류가 발생했습니다',
      required_field: '필수 항목입니다',

      // Install App
      install_app: '앱 설치하기',
      install_ios: 'App Store에서 다운로드',
      install_android: 'Play Store에서 다운로드'
    }
  },
  en: {
    translation: {
      // Common
      app_name: 'Digital Business Card',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      add: 'Add',
      remove: 'Remove',
      search: 'Search',
      back: 'Back',
      next: 'Next',
      done: 'Done',

      // Navigation
      my_cards: 'My Cards',
      card_collection: 'Card Collection',
      settings: 'Settings',

      // Card Creation
      create_card: 'Create Card',
      edit_card: 'Edit Card',
      card_info: 'Card Information',
      name: 'Name',
      photo: 'Photo',
      address: 'Address',
      select_photo: 'Select Photo',
      take_photo: 'Take Photo',
      from_gallery: 'From Gallery',

      // Dynamic Fields
      phone: 'Phone',
      email: 'Email',
      website: 'Website',
      fax: 'FAX',
      add_phone: 'Add Phone',
      add_email: 'Add Email',
      add_website: 'Add Website',
      add_fax: 'Add FAX',
      label: 'Label',
      value: 'Value',

      // Field Labels
      office: 'Office',
      personal: 'Personal',
      mobile: 'Mobile',
      work: 'Work',
      home: 'Home',
      main: 'Main Office',
      branch: 'Branch',

      // Templates
      select_template: 'Select Template',
      template: 'Template',

      // Themes
      select_theme: 'Select Theme',
      blue_theme: 'Blue Theme',
      pink_theme: 'Pink Theme',

      // Privacy
      privacy_setting: 'Privacy Setting',
      public: 'Public',
      link_only: 'Link Only',
      private: 'Private',

      // Share & QR
      share_card: 'Share Card',
      qr_code: 'QR Code',
      scan_qr: 'Scan QR',
      download_qr: 'Download QR Code',

      // Account
      account: 'Account',
      link_account: 'Link Account',
      link_google: 'Link Google Account',
      link_apple: 'Link Apple Account',
      anonymous_user: 'Anonymous User',
      linked_account: 'Linked Account',

      // Messages
      copied: 'Copied',
      email_copied: 'Email address copied',
      fax_copied: 'FAX number copied',
      card_saved: 'Card saved',
      card_deleted: 'Card deleted',
      max_fields: 'Maximum 3 items allowed',

      // Errors
      error: 'Error',
      error_loading: 'Error loading data',
      error_saving: 'Error saving data',
      required_field: 'This field is required',

      // Install App
      install_app: 'Install App',
      install_ios: 'Download on App Store',
      install_android: 'Get it on Play Store'
    }
  },
  zh: {
    translation: {
      // Common
      app_name: '数字名片',
      save: '保存',
      cancel: '取消',
      delete: '删除',
      edit: '编辑',
      add: '添加',
      remove: '移除',
      search: '搜索',
      back: '返回',
      next: '下一步',
      done: '完成',

      // Navigation
      my_cards: '我的名片',
      card_collection: '名片夹',
      settings: '设置',

      // Card Creation
      create_card: '创建名片',
      edit_card: '编辑名片',
      card_info: '名片信息',
      name: '姓名',
      photo: '照片',
      address: '地址',
      select_photo: '选择照片',
      take_photo: '拍照',
      from_gallery: '从相册选择',

      // Dynamic Fields
      phone: '电话',
      email: '邮箱',
      website: '网站',
      fax: '传真',
      add_phone: '添加电话',
      add_email: '添加邮箱',
      add_website: '添加网站',
      add_fax: '添加传真',
      label: '标签',
      value: '值',

      // Field Labels
      office: '办公室',
      personal: '个人',
      mobile: '手机',
      work: '工作',
      home: '家庭',
      main: '总部',
      branch: '分部',

      // Templates
      select_template: '选择模板',
      template: '模板',

      // Themes
      select_theme: '选择主题',
      blue_theme: '蓝色主题',
      pink_theme: '粉色主题',

      // Privacy
      privacy_setting: '隐私设置',
      public: '公开',
      link_only: '仅限链接',
      private: '私密',

      // Share & QR
      share_card: '分享名片',
      qr_code: '二维码',
      scan_qr: '扫描二维码',
      download_qr: '下载二维码',

      // Account
      account: '账户',
      link_account: '关联账户',
      link_google: '关联谷歌账户',
      link_apple: '关联苹果账户',
      anonymous_user: '匿名用户',
      linked_account: '已关联账户',

      // Messages
      copied: '已复制',
      email_copied: '邮箱地址已复制',
      fax_copied: '传真号码已复制',
      card_saved: '名片已保存',
      card_deleted: '名片已删除',
      max_fields: '最多可添加3项',

      // Errors
      error: '错误',
      error_loading: '加载数据时出错',
      error_saving: '保存数据时出错',
      required_field: '此项为必填',

      // Install App
      install_app: '安装应用',
      install_ios: '在App Store下载',
      install_android: '在Play Store下载'
    }
  },
  ja: {
    translation: {
      // Common
      app_name: 'デジタル名刺',
      save: '保存',
      cancel: 'キャンセル',
      delete: '削除',
      edit: '編集',
      add: '追加',
      remove: '削除',
      search: '検索',
      back: '戻る',
      next: '次へ',
      done: '完了',

      // Navigation
      my_cards: 'マイ名刺',
      card_collection: '名刺ホルダー',
      settings: '設定',

      // Card Creation
      create_card: '名刺を作成',
      edit_card: '名刺を編集',
      card_info: '名刺情報',
      name: '名前',
      photo: '写真',
      address: '住所',
      select_photo: '写真を選択',
      take_photo: '写真を撮る',
      from_gallery: 'ギャラリーから選択',

      // Dynamic Fields
      phone: '電話',
      email: 'メール',
      website: 'ウェブサイト',
      fax: 'FAX',
      add_phone: '電話を追加',
      add_email: 'メールを追加',
      add_website: 'ウェブサイトを追加',
      add_fax: 'FAXを追加',
      label: 'ラベル',
      value: '値',

      // Field Labels
      office: 'オフィス',
      personal: '個人',
      mobile: '携帯',
      work: '仕事',
      home: '自宅',
      main: '本社',
      branch: '支店',

      // Templates
      select_template: 'テンプレート選択',
      template: 'テンプレート',

      // Themes
      select_theme: 'テーマ選択',
      blue_theme: 'ブルーテーマ',
      pink_theme: 'ピンクテーマ',

      // Privacy
      privacy_setting: 'プライバシー設定',
      public: '公開',
      link_only: 'リンクのみ',
      private: '非公開',

      // Share & QR
      share_card: '名刺を共有',
      qr_code: 'QRコード',
      scan_qr: 'QRスキャン',
      download_qr: 'QRコードをダウンロード',

      // Account
      account: 'アカウント',
      link_account: 'アカウント連携',
      link_google: 'Googleアカウント連携',
      link_apple: 'Appleアカウント連携',
      anonymous_user: '匿名ユーザー',
      linked_account: '連携済みアカウント',

      // Messages
      copied: 'コピーしました',
      email_copied: 'メールアドレスをコピーしました',
      fax_copied: 'FAX番号をコピーしました',
      card_saved: '名刺を保存しました',
      card_deleted: '名刺を削除しました',
      max_fields: '最大3つまで追加できます',

      // Errors
      error: 'エラー',
      error_loading: 'データの読み込み中にエラーが発生しました',
      error_saving: 'データの保存中にエラーが発生しました',
      required_field: 'この項目は必須です',

      // Install App
      install_app: 'アプリをインストール',
      install_ios: 'App Storeでダウンロード',
      install_android: 'Play Storeで入手'
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'ko', // default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
