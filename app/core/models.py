from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Float, ForeignKey, func, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'tb_user_info'

    USER_MNG_ID = Column(BigInteger, primary_key=True, nullable=False, comment='사용자 관리 ID')
    USCL_CD = Column(String(8), nullable=False, default='USCL0001', comment='사용자 코드')
    LOGI_CD = Column(String(8), nullable=False, default='LOGI0001', comment='소설로그인 코드')
    USER_ID = Column(String(100), nullable=False, comment='사용자 ID')
    PSSWRD = Column(String(100), nullable=False, comment='비밀번호')
    USER_NM = Column(String(50), nullable=False, comment='사용자명')
    DISPLAY_NM = Column(String(50), comment='보이는 이름')
    EMAIL = Column(String(255), nullable=False, comment='이메일')
    PHONE_NO = Column(String(255), comment='휴대전화번호')
    LOGIN_DT = Column(DateTime, default=func.now(), comment='로그인 일시')
    PSSWRD_ERR_NT = Column(Integer, default=0, comment='비밀번호 오류 횟수')
    PSSWRD_LAST_CHANGE_DT = Column(DateTime, default=func.now(), comment='패스워드 마지막 변경일시')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class Tag(Base):
    __tablename__ = 'tb_tags'

    TAG_ID = Column(BigInteger, primary_key=True, comment='태그 아이디')
    TAG_NAME = Column(String(255), nullable=False, comment='태그명')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class Role(Base):
    __tablename__ = 'tb_role'

    ROLE_ID = Column(BigInteger, primary_key=True, comment='권한 ID')
    ROLE_NM = Column(String(20), nullable=False, comment='권한 명')
    ROLE_KR_NM = Column(String(20), nullable=False, comment='권한 한글명')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class CommonCodeGroup(Base):
    __tablename__ = 'tb_common_code_group'

    CODE_GROUP_ID = Column(BigInteger, primary_key=True, comment='그룹 아이디')
    CODE_GROUP_CD = Column(String(8), nullable=False, comment='그룹 코드')
    CODE_GROUP_NM = Column(String(50), nullable=False, comment='그룹명')
    DESCRIPTION = Column(String(50), comment='설명')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class CommonCode(Base):
    __tablename__ = 'tb_common_code'

    CODE_ID = Column(BigInteger, primary_key=True, comment='코드 아이디')
    CODE_CD = Column(String(8), nullable=False, comment='코드 코드')
    LANG_CD = Column(String(8), nullable=False, default='LANT0000', comment='언어 코드')
    CODE_NM = Column(String(50), nullable=False, comment='코드명')
    DESCRIPTION = Column(String(50), comment='설명')
    CODE_GROUP_CD = Column(String(8), comment='부모코드')
    CODE_ORDER = Column(Integer, comment='코드 정렬')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class AssetStore(Base):
    __tablename__ = 'tb_asset_store'

    ASSET_ID = Column(String(200), primary_key=True, comment='에셋 아이디')
    ASSET_TITLE = Column(String(255), nullable=False, comment='에셋 제목')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    CTGRY_CD = Column(String(16), nullable=False, comment='카테고리 코드')
    CPRT_CD = Column(String(8), nullable=False, comment='저작권 코드')
    CVTT_CD = Column(String(8), nullable=False, comment='변환타입 코드')
    ASPR_CD = Column(String(8), comment='판매가격옵션 코드')
    DESCRIPTION = Column(Text, comment='에셋 설명')
    PUBLIC_YN = Column(String(1), nullable=False, default='Y', comment='공개 여부')
    PICK_YN = Column(String(1), nullable=False, default='N', comment='관리자 픽 여부')
    READ_CNT = Column(Integer, nullable=False, default=0, comment='조회수')
    LIKE_CNT = Column(Integer, nullable=False, default=0, comment='좋아요')
    FILE_UUID = Column(String(200), comment='파일 UUID')
    THUM_MODEL_ID = Column(BigInteger, comment='썸네일 파일 아이디')
    COMMENT_YN = Column(String(1), comment='댓글허용 여부')
    TEXTURE_YN = Column(String(1), nullable=False, default='Y', comment='텍스처검사 허용 여부')
    TASK_TYPE = Column(String(10), comment='txtto3d imgto3d')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    ASSET_TYPE = Column(String(10), comment='에셋타입')
    #STATUS = Column(String(11), nullable=False, comment='public or private')

    nodes = relationship("NodeStore", back_populates="asset")

class AssetCategory(Base):
    __tablename__ = 'tb_asset_category'

    CTGRY_ID = Column(BigInteger, primary_key=True, comment='Category ID')
    CTGRY_CD = Column(String(16), nullable=False, comment='Category Code')
    CTGRY_NM = Column(String(50), nullable=False, comment='Category Name')
    CTGRY_PCD = Column(String(16), nullable=True, default=None, comment='Parent Category Code')
    CTGRY_DEPTH = Column(Integer, nullable=True, default=None, comment='Category Depth')
    CTGRY_NAV = Column(String(100), nullable=True, default=None, comment='Category Navigation')
    CTGRY_ORDER = Column(Integer, nullable=True, default=None, comment='Category Order')
    CTGRY_DESC = Column(String(100), nullable=True, default=None, comment='Category Description')
    CTGRY_ICON = Column(String(100), nullable=True, default=None, comment='Category Icon')
    LANG_CD = Column(String(8), nullable=True, default=None, comment='Language Code')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, default='system', comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, default='system', comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')

class AssetDownload(Base):
    __tablename__ = 'tb_asset_download'

    DOWN_ID = Column(BigInteger, primary_key=True, comment='Download ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='User Management ID')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')

class AssetLikes(Base):
    __tablename__ = 'tb_asset_likes'

    LIKE_ID = Column(BigInteger, primary_key=True, comment='Like ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='User Management ID')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')

class AssetRatings(Base):
    __tablename__ = 'tb_asset_ratings'

    RATE_ID = Column(BigInteger, primary_key=True, comment='Rating ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='User Management ID')
    RATING = Column(Numeric(3, 2), nullable=True, default=None, comment='Rating')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')

class AssetSales(Base):
    __tablename__ = 'tb_asset_sales'

    SALES_ID = Column(BigInteger, primary_key=True, comment='Sales ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='User Management ID')
    SALES_PRICE = Column(Numeric(10, 2), nullable=False, comment='Asset Sales Price')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')

class AssetSalesHist(Base):
    __tablename__ = 'tb_asset_sales_hist'

    SALES_HIST_ID = Column(BigInteger, primary_key=True, comment='Sales History ID')
    SALES_ID = Column(BigInteger, nullable=False, comment='Sales ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='User Management ID')
    SALES_PRICE = Column(Numeric(10, 2), nullable=False, comment='Asset Sales Price')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')


class AssetTags(Base):
    __tablename__ = 'tb_asset_tags'

    ASSET_TAGS_ID = Column(BigInteger, primary_key=True, comment='Asset Tag ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    TAG_ID = Column(BigInteger, nullable=False, comment='Tag ID')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')

class EcmrcCart(Base):
    __tablename__ = 'tb_ecmrc_cart'

    CART_ID = Column(BigInteger, primary_key=True, comment='Cart ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='User Management ID')
    NOLOGIN_ID = Column(String(200), nullable=True, comment='Non-Login Identifier ID')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')

class EcmrcOrder(Base):
    __tablename__ = 'tb_ecmrc_order'

    ORDER_ID = Column(String(200), primary_key=True, comment='Order ID')
    ASSET_ID = Column(String(200), nullable=False, comment='Asset ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='User Management ID')
    ORDER_PRICE = Column(Numeric(10, 2), nullable=False, comment='Order Price')
    ODST_CD = Column(String(8), nullable=False, comment='Order Status Code')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='Use Flag')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='Delete Flag')
    REG_USER_ID = Column(String(100), nullable=False, comment='Registration User ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='Registration Date')
    MOD_USER_ID = Column(String(100), nullable=False, comment='Modification User ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='Modification Date')


class EcmrcPayment(Base):
    __tablename__ = 'tb_ecmrc_payment'

    PAYMENT_ID = Column(BigInteger, primary_key=True, comment='결제 아이디')
    ORDER_ID = Column(String(200), nullable=False, comment='주문 아이디')
    PAYMENT_AMOUNT = Column(Numeric(10, 2), nullable=False, comment='결제 금액')
    CANCLE_AMOUNT = Column(Numeric(10, 2), nullable=True, default=None, comment='결제 취소 금액')
    PYMT_CD = Column(String(8), nullable=False, comment='결제 수단 코드')
    PYST_CD = Column(String(8), nullable=False, comment='결제 상태 코드')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class EcmrcPaymentHist(Base):
    __tablename__ = 'tb_ecmrc_payment_hist'

    PAYMENT_HIST_ID = Column(BigInteger, primary_key=True, comment='결제 히스토리 아이디')
    PAYMENT_ID = Column(BigInteger, nullable=False, comment='결제 아이디')
    ORDER_ID = Column(String(200), nullable=False, comment='주문 아이디')
    PAYMENT_AMOUNT = Column(Numeric(10, 2), nullable=False, comment='결제 금액')
    CANCLE_AMOUNT = Column(Numeric(10, 2), nullable=True, default=None, comment='결제 취소 금액')
    PYMT_CD = Column(String(8), nullable=False, comment='결제 수단 코드')
    PYST_CD = Column(String(8), nullable=False, comment='결제 상태 코드')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    LOGIN_DT = Column(DateTime, nullable=True, comment='로그인 일시')


class FileMaster(Base):
    __tablename__ = 'tb_file_master'

    FILE_MASTER_ID = Column(BigInteger, primary_key=True, comment='모델 업로드 ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='회원 ID')
    FILE_UUID = Column(String(200), nullable=False, comment='업로드명')
    UPLOAD_STATUS_CD = Column(String(5), nullable=False)
    UPLOAD_FILE_COUNT = Column(Integer, nullable=True, default=None, comment='업로드한 파일 개수')
    UPLOAD_FILE_PATH = Column(String(500), nullable=False, comment='업로드 파일경로')
    NERF_STATUS_CD = Column(String(5), nullable=True, default=None, comment='변환 구분( 01:업로드완료, 02: 변환진행중, 03: 변환완료, 04: 에러)')
    NERF_FILE_PATH = Column(String(500), nullable=True, default=None)
    CNVRT_CPTN_DT = Column(DateTime, nullable=True, default=None, comment='변환 완료 일시')
    REG_USER_ID = Column(String(100), nullable=True, default=None, comment='등록 사용자 ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='등록일시')
    MOD_USER_ID = Column(String(100), nullable=True, default=None, comment='변경 사용자 ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='변경일시')
    #FIELD = Column(String(255), nullable=True)


class FileMasterTemp(Base):
    __tablename__ = 'tb_file_master_temp'

    FILE_MASTER_ID = Column(BigInteger, primary_key=True, comment='모델 업로드 ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='회원 ID')
    FILE_UUID = Column(String(200), nullable=False, comment='업로드명')
    UPLOAD_STATUS_CD = Column(String(5), nullable=False)
    UPLOAD_FILE_COUNT = Column(Integer, nullable=True, default=None, comment='업로드한 파일 개수')
    UPLOAD_FILE_PATH = Column(String(500), nullable=False, comment='업로드 파일경로')
    NERF_STATUS_CD = Column(String(5), nullable=True, default=None, comment='변환 구분( 01:업로드완료, 02: 변환진행중, 03: 변환완료, 04: 에러)')
    NERF_FILE_PATH = Column(String(500), nullable=True, default=None)
    CNVRT_CPTN_DT = Column(DateTime, nullable=True, default=None, comment='변환 완료 일시')
    REG_USER_ID = Column(String(100), nullable=True, default=None, comment='등록 사용자 ID')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='등록일시')
    MOD_USER_ID = Column(String(100), nullable=True, default=None, comment='변경 사용자 ID')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='변경일시')


class FileMedia(Base):
    __tablename__ = 'tb_file_media'

    FILE_MEDIA_ID = Column(BigInteger, primary_key=True, comment='PK')
    FILE_UUID = Column(String(200), nullable=False, comment='업로드 UUID')
    FILE_SEQ = Column(Integer, nullable=True, default=None, comment='업로드 시퀀스')
    ORGN_FILE_NM = Column(String(300), nullable=False, comment='원본 파일명')
    CHNG_FILE_NM = Column(String(300), nullable=False, comment='수정된 파일명')
    FILE_EXT = Column(String(100), nullable=False, comment='파일 확장자')
    FILE_MEDIA_TYPE = Column(String(50), nullable=True, default=None)
    FILE_OFFSET = Column(BigInteger, nullable=True, default=None, comment='파일 오프셋')
    FILE_SIZE = Column(BigInteger, nullable=False, comment='파일 크기')
    FILE_UPLOAD_YN = Column(String(1), nullable=True, default=None, comment='파일 업로드 여부')
    REG_USER_ID = Column(String(100), nullable=True, default=None, comment='등록자')
    REG_DT = Column(DateTime, nullable=True, default=func.now(), comment='등록일시')
    MOD_USER_ID = Column(String(100), nullable=True, default=None, comment='수정자')
    MOD_DT = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())


class FileModel(Base):
    __tablename__ = 'tb_file_model'

    FILE_MODEL_ID = Column(BigInteger, primary_key=True, comment='PK')
    FILE_UUID = Column(String(200), nullable=False, comment='asset uuid')
    ORGN_FILE_NM = Column(String(300), nullable=False, comment='original file name')
    CHNG_FILE_NM = Column(String(300), nullable=False, comment='changed file name')
    FILE_SEQ = Column(Integer, nullable=True, default=None)
    FILE_EXT = Column(String(100), nullable=False, comment='filename extension')
    FILE_MEDIA_TYPE = Column(String(50), nullable=True, default=None, comment='media type')
    FILE_SIZE = Column(BigInteger, nullable=False, comment='file size')
    FILE_UPLOAD_YN = Column(String(1), nullable=True, default=None, comment='(Y/N) flag of file\'s upload status')
    CTGRY_CD = Column(String(50), nullable=False, comment='category code name')
    REG_USER_ID = Column(String(100), nullable=True, default=None, comment='user registering row')
    REG_DT = Column(DateTime, nullable=True, default=func.now(), comment='registered date')
    MOD_USER_ID = Column(String(100), nullable=True, default=None, comment='user modifing row')
    MOD_DT = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now(), comment='modified date')

class FileModelTemp(Base):
    __tablename__ = 'tb_file_model_temp'

    FILE_MODEL_ID = Column(BigInteger, primary_key=True, comment='PK')
    FILE_UUID = Column(String(200), nullable=False, comment='asset uuid')
    ORGN_FILE_NM = Column(String(300), nullable=False, comment='original file name')
    CHNG_FILE_NM = Column(String(300), nullable=False, comment='changed file name')
    FILE_SEQ = Column(Integer, nullable=True, default=None)
    FILE_EXT = Column(String(100), nullable=False, comment='filename extension')
    FILE_MEDIA_TYPE = Column(String(50), nullable=True, default=None, comment='media type')
    FILE_SIZE = Column(BigInteger, nullable=False, comment='file size')
    FILE_UPLOAD_YN = Column(String(1), nullable=True, default=None, comment='(Y/N) flag of file\'s upload status')
    CTGRY_CD = Column(String(50), nullable=False, comment='category code name')
    REG_USER_ID = Column(String(100), nullable=True, default=None, comment='user registering row')
    REG_DT = Column(DateTime, nullable=True, default=func.now(), comment='registered date')
    MOD_USER_ID = Column(String(100), nullable=True, default=None, comment='user modifying row')
    MOD_DT = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now(), comment='modified date')


class FileStorageDeprecated(Base):
    __tablename__ = 'tb_file_storage_deprecated'

    FILE_STORAGE_ID = Column(BigInteger, primary_key=True, comment='파일 ID')
    FILE_UUID = Column(String(200), nullable=True, default=None, comment='파일 순번')
    FILE_COUNT = Column(Integer, nullable=True, default=None, comment='파일 구분')
    ORGN_FILE_NM = Column(String(300), nullable=True, default=None, comment='원본파일명')
    CHNG_FILE_NM = Column(String(300), nullable=True, default=None, comment='서버에 저장된 파일명')
    FILE_PATH = Column(String(200), nullable=False, comment='파일 경로명')
    FILE_SIZE = Column(BigInteger, nullable=True, default=None, comment='파일 크기')
    FILE_EXT = Column(String(5), nullable=True, default=None, comment='파일 확장자')
    FILE_MEDIA_TYPE = Column(String(50), nullable=True, default=None, comment='파일 미디어타입')
    FILE_OFFSET = Column(BigInteger, nullable=True, default=None, comment='파일 오프셋 전체값')
    FILE_UPLOAD_YN = Column(String(1), nullable=True, default=None, comment='파일 업로드 완료 여부')
    REG_USER_ID = Column(String(100), nullable=True, default=None, comment='등록 사용자 ID')
    REG_DT = Column(DateTime, nullable=True, default=func.now(), comment='등록일시')
    MOD_USER_ID = Column(String(100), nullable=True, default=None, comment='변경 사용자 ID')
    MOD_DT = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now(), comment='변경일시')

class SbscProduct(Base):
    __tablename__ = 'tb_sbsc_product'

    SBSC_ID = Column(BigInteger, primary_key=True, comment='구독 아이디')
    SBSC_CD = Column(String(8), nullable=False, comment='구독 타입')
    SBSC_PRICE = Column(Numeric(10, 2), nullable=False, comment='구독 가격')
    SBSC_START_DT = Column(DateTime, nullable=True, default=None, comment='구독 상품 개시 일자')
    SBSC_END_DT = Column(DateTime, nullable=True, default=None, comment='구독 상품 종료 일자')
    RENEW_YN = Column(String(1), nullable=False, default='N', comment='자동갱신 여부')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class SbscSign(Base):
    __tablename__ = 'tb_sbsc_sign'

    SIGN_ID = Column(BigInteger, primary_key=True, comment='구독 가입 아이디')
    SBSC_ID = Column(BigInteger, nullable=False, comment='구독 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    SBST_CD = Column(String(8), nullable=False, comment='구독 상태')
    SIGN_START_DT = Column(DateTime, nullable=True, default=None, comment='구독 개시 일자')
    SIGN_END_DT = Column(DateTime, nullable=True, default=None, comment='구독 종료 일자')
    SIGN_END_MEMO = Column(Text, nullable=True, default=None, comment='구독 종료 이유')
    RENEW_YN = Column(String(1), nullable=False, default='N', comment='자동갱신 여부')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class UserLoginHistory(Base):
    __tablename__ = 'tb_user_login_history'

    LOGIN_HISTORY_ID = Column(BigInteger, primary_key=True, comment='로그인 기록 ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 아이디')
    LOGIN_STATUS = Column(String(8), nullable=True, comment='로그인 상태')
    LOGIN_DT = Column(DateTime, nullable=False, default=func.now(), comment='로그인 날짜')
    LOGIN_IP = Column(String(100), nullable=True, default=None, comment='로그인 IP')
    LOGIN_USER_AGENT = Column(String(1000), nullable=True, default=None, comment='로그인 에이전트')
    LOGIN_URL = Column(String(50), nullable=True, default=None, comment='로그인 URL')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class UserRefreshToken(Base):
    __tablename__ = 'tb_user_refresh_token'

    REFRESH_TOKEN_ID = Column(BigInteger, primary_key=True, comment='리프레시 토큰 ID')
    TOKEN = Column(String(500), nullable=False, comment='리프레시 토큰')
    EXPIRATION_DT = Column(DateTime, nullable=False, default=func.now(), comment='만료일시')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class UserRole(Base):
    __tablename__ = 'tb_user_role'

    USER_ROLE_ID = Column(BigInteger, primary_key=True, comment='사용자 권한 ID')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    ROLE_ID = Column(BigInteger, nullable=False, comment='권한 ID')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class UserSocial(Base):
    __tablename__ = 'tb_user_social'

    SOCIAL_ID = Column(BigInteger, primary_key=True, comment='소설 로그인 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    EMAIL = Column(String(255), nullable=False, comment='이메일')
    LOGI_CD = Column(String(8), nullable=False, comment='로그인 코드')
    SOCIAL_KEY = Column(String(45), nullable=True, default=None, comment='소셜 로그인 키')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class UserAuth(Base):
    __tablename__ = 'tb_user_auth'

    AUTH_ID = Column(BigInteger, primary_key=True, comment='유저 인증 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    AUTH_CD = Column(String(8), nullable=False, comment='인증타입')
    EMAIL = Column(String(255), nullable=False, comment='이메일')
    AUTH_CODE = Column(String(6), nullable=False, comment='인증코드')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class AssetComments(Base):
    __tablename__ = 'tb_asset_comments'

    COMMENTS_ID = Column(BigInteger, primary_key=True, comment='댓글 아이디')
    ASSET_ID = Column(String(200), nullable=False, comment='애셋 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    PARENT_ID = Column(BigInteger, nullable=True, default=None, comment='댓글 부모 아이디')
    COMMENTS = Column(Text, nullable=False, comment='댓글')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    
class AssetSellerInfo(Base):
    __tablename__ = 'tb_asset_seller_info'

    SELLER_ID = Column(BigInteger, primary_key=True, comment='판매자 정보 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    COUNTRY = Column(String(100), nullable=True, default=None, comment='나라')
    CITY = Column(String(100), nullable=True, default=None, comment='도시')
    ADDRESS = Column(String(200), nullable=True, default=None, comment='주소')
    BANK = Column(String(100), nullable=True, default=None, comment='은행')
    ACCOUNT_NUM = Column(String(100), nullable=True, default=None, comment='번호')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class AssetRequest(Base):
    __tablename__ = 'tb_asset_request'

    REQUEST_ID = Column(BigInteger, primary_key=True, comment='요청 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    TITLE = Column(String(100), nullable=False, comment='제목')
    CONTENTS = Column(Text, nullable=True, default=None, comment='내용')
    RECIPIENT = Column(String(100), nullable=True, default=None, comment='받는이')
    PARENT_ID = Column(BigInteger, nullable=True, default=None, comment='부모아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')



class NodeComments(Base):
    __tablename__ = 'tb_node_comments'

    COMMENT_ID = Column(BigInteger, primary_key=True, comment='댓글 아이디')
    NODE_ID = Column(BigInteger, nullable=False, comment='node id', primary_key=True)
    ASSET_ID = Column(String(200), nullable=False, comment='에셋 아이디', primary_key=True)
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    PARENT_ID = Column(BigInteger, nullable=True, default=None, comment='댓글 부모 아이디')
    COMMENTS = Column(Text, nullable=False, comment='댓글')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class NodeLikes(Base):
    __tablename__ = 'tb_node_likes'

    LIKE_ID = Column(BigInteger, primary_key=True, comment='좋아요 아이디')
    NODE_ID = Column(BigInteger, nullable=False, comment='node id', primary_key=True)
    ASSET_ID = Column(String(200), nullable=False, comment='에셋 아이디', primary_key=True)
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='수정일시')
                    
class NodeStore(Base):
    __tablename__ = 'tb_node_store'

    NODE_ID = Column(String(200), primary_key=True, comment='node id')
    ASSET_ID = Column(String(200), ForeignKey('tb_asset_store.ASSET_ID'), nullable=False, comment='에셋 아이디')
    NODE_TITLE = Column(String(255), nullable=False, comment='node 제목')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    NODE_DESCRIPTION = Column(String, nullable=True, default=None, comment='node 설명')
    ANCHOR_UUID = Column(String(255), nullable=False, comment='anchor UUID')
    LATITUDE = Column(Float, nullable=False, comment='latitude')
    LONGITUDE = Column(Float, nullable=False, comment='longitude')
    #THUM_MODEL_ID = Column(BigInteger, nullable=True, default=None, comment='썸네일 파일 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    NODE_JSON_PATH = Column(String(255), nullable=False, comment='NODE_JSON_PATH')
    NODE_JSON_NAME = Column(String(255), nullable=False, comment='NODE_JSON_NAME')
    PUBLIC_YN = Column(String(1), nullable=False, comment='public or private')

    asset = relationship("AssetStore", back_populates="nodes")
    videos = relationship("VideoStore", back_populates="node")


class VideoStore(Base):
    __tablename__ = 'tb_video_store'

    VIDEO_ID = Column(String(200), primary_key=True, comment='video id')
    NODE_ID = Column(String(200), ForeignKey('tb_node_store.NODE_ID'), nullable=False, comment='node id')
    ASSET_ID = Column(String(200), ForeignKey('tb_asset_store.ASSET_ID'), nullable=False, comment='에셋 아이디')
    VIDEO_TITLE = Column(String(255), nullable=False, comment='video 제목')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    VIDEO_DESCRIPTION = Column(String, nullable=True, default=None, comment='video 설명')
    #THUM_MODEL_ID = Column(BigInteger, ForeignKey('tb_file_model.file_model_id'), nullable=True, comment='썸네일 파일 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    VIDEO_FILE_PATH = Column(String(255), nullable=False, comment='VIDEO_FILE_PATH')
    VIDEO_FILE_NAME = Column(String(255), nullable=False, comment='VIDEO_FILE_NAME')
    PUBLIC_YN = Column(String(11), nullable=False, comment='public or private')

    node = relationship("NodeStore", back_populates="videos")



class AnchorStore(Base):
    __tablename__ = 'tb_anchor_store'

    ANCHOR_ID = Column(String(200), primary_key=True, comment='anchor id')
    ANCHOR_TITLE = Column(String(255), nullable=False, comment='anchor 제목')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    ANCHOR_UUID = Column(String(255), nullable=False, comment='anchor UUID')
    LATITUDE = Column(Float, nullable=False, comment='latitude')
    LONGITUDE = Column(Float, nullable=False, comment='longitude')
    #THUM_MODEL_ID = Column(BigInteger, ForeignKey('tb_file_model.file_model_id'), nullable=True, comment='썸네일 파일 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    PUBLIC_YN = Column(String(11), nullable=False, comment='public or private')


class FileUpload(Base):
    __tablename__ = 'tb_file_upload'

    FILE_UPLOAD_ID = Column(BigInteger, primary_key=True, comment='uploaded file id')
    FILE_UPLAOD_UUID = Column(String(255), nullable=False, comment='uploaded file uuid')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='사용자 관리 ID')
    FILE_UPLOAD_PATH = Column(String(255), nullable=False, comment='FILE_UPLOAD_PATH')
    FILE_UPLOAD_NAME = Column(String(255), nullable=False, comment='FILE_UPLOAD_NAME')
    FILE_UPLOAD_COUNT = Column(String(255), nullable=False, comment='FILE_UPLOAD_COUNT')
    FILE_UPLOAD_CONVERSION_TYPE = Column(String(255), nullable=True, default=None, comment='FILE_UPLOAD_CONVERSION_TYPE')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    FILE_UPLOAD_STATUS = Column(String(255), nullable=False, comment='FILE_UPLOAD_STATUS')


class FollowFriend(Base):
    __tablename__ = 'tb_follow_friend'

    FOLLOW_ID = Column(BigInteger, primary_key=True, comment='follow id')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')
    FOLLOWER_ID = Column(String(200), nullable=False, comment='follower id')

class NodeTags(Base):
    __tablename__ = 'tb_node_tags'

    NODE_TAGS_ID = Column(BigInteger, primary_key=True, comment='node 태그 아이디')
    NODE_ID = Column(BigInteger, nullable=False, comment='node id')
    ASSET_ID = Column(String(200), nullable=False, comment='에셋 아이디')
    TAG_ID = Column(BigInteger, nullable=False, comment='태그 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

class NodeSaves(Base):
    __tablename__ = 'tb_node_saves'

    SAVE_ID = Column(BigInteger, primary_key=True, comment='save 아이디')
    NODE_ID = Column(BigInteger, nullable=False, comment='node id')
    ASSET_ID = Column(String(200), nullable=False, comment='에셋 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class AssetSaves(Base):
    __tablename__ = 'tb_asset_saves'

    SAVE_ID = Column(BigInteger, primary_key=True, comment='save 아이디')
    ASSET_ID = Column(String(200), nullable=False, comment='애셋 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')


class Alarm(Base):
    __tablename__ = 'tb_alarm'

    ALAM_ID = Column(BigInteger, primary_key=True, comment='알람 아이디')
    ASSET_ID = Column(String(200), nullable=False, comment='애셋 아이디')
    USER_MNG_ID = Column(BigInteger, nullable=False, comment='유저 관리 아이디')
    ALAM_CD = Column(String(8), nullable=False, comment='알람코드 아이디')
    ALAM_MSG = Column(String(255), nullable=False, comment='알람메시지')
    READ_YN = Column(String(1), nullable=False, default='N', comment='읽음유무')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용유무')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')