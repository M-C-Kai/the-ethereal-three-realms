.class public final Lpmsj/work/e/ad;
.super Lpmsj/work/d/c;


# instance fields
.field private K:Lpmsj/work/d/l;

.field private L:[Ljava/util/Vector;

.field private M:Lpmsj/work/d/i;

.field private N:[I

.field private O:[Z

.field private P:Ljava/util/Vector;

.field private final Q:B

.field private final R:B

.field private final S:B

.field private final T:B

.field private final U:B

.field private final V:B

.field private W:B

.field private X:B

.field private final a:I

.field private final b:I

.field private final c:I

.field private final d:I

.field private e:Lpmsj/work/d/k;

.field private f:Lpmsj/work/d/l;


# direct methods
.method public constructor <init>()V
    .locals 3

    const/4 v2, 0x1

    const/4 v1, 0x0

    invoke-direct {p0}, Lpmsj/work/d/c;-><init>()V

    const v0, 0x4e9d1

    iput v0, p0, Lpmsj/work/e/ad;->a:I

    const v0, 0x4e9d2

    iput v0, p0, Lpmsj/work/e/ad;->b:I

    const v0, 0x4e9d3

    iput v0, p0, Lpmsj/work/e/ad;->c:I

    const v0, 0x4e9d4

    iput v0, p0, Lpmsj/work/e/ad;->d:I

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/e/ad;->P:Ljava/util/Vector;

    iput-byte v1, p0, Lpmsj/work/e/ad;->Q:B

    iput-byte v2, p0, Lpmsj/work/e/ad;->R:B

    const/4 v0, 0x2

    iput-byte v0, p0, Lpmsj/work/e/ad;->S:B

    const/4 v0, 0x3

    iput-byte v0, p0, Lpmsj/work/e/ad;->T:B

    iput-byte v1, p0, Lpmsj/work/e/ad;->U:B

    iput-byte v2, p0, Lpmsj/work/e/ad;->V:B

    iput-byte v1, p0, Lpmsj/work/e/ad;->W:B

    iput-byte v2, p0, Lpmsj/work/e/ad;->X:B

    return-void
.end method

.method private C(I)B
    .locals 3

    const/4 v0, 0x0

    move v1, v0

    :goto_0
    iget-object v0, p0, Lpmsj/work/e/ad;->P:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/e/ad;->P:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [La/c/i;

    iget-byte v2, p0, Lpmsj/work/e/ad;->W:B

    aget-object v0, v0, v2

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    if-ne v0, p1, :cond_0

    move v0, v1

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v1, 0x1

    int-to-byte v0, v0

    move v1, v0

    goto :goto_0

    :cond_1
    const/4 v0, -0x1

    goto :goto_1
.end method

.method private static a(ILjava/util/Vector;)I
    .locals 4

    const/4 v3, 0x0

    invoke-virtual {p1}, Ljava/util/Vector;->size()I

    move-result v1

    move v2, v3

    :goto_0
    if-ge v2, v1, :cond_1

    invoke-virtual {p1, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {v0, v3}, La/c/a;->a(I)I

    move-result v0

    if-ne p0, v0, :cond_0

    move v0, v2

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, -0x1

    goto :goto_1
.end method

.method private a(La/c/a;)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    const/4 v1, 0x1

    invoke-virtual {p1, v1}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    const/4 v1, 0x2

    invoke-virtual {p1, v1}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    iget-object v2, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    div-int/lit8 v2, v2, 0x3

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/l;->a(Ljava/lang/String;I)V

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    const/4 v1, 0x3

    invoke-virtual {p1, v1}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    return-void
.end method

.method private i()V
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/ad;->N:[I

    iget-object v1, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v1}, Lpmsj/work/d/k;->f()I

    move-result v1

    aget v0, v0, v1

    if-lez v0, :cond_0

    iget-object v1, p0, Lpmsj/work/e/ad;->M:Lpmsj/work/d/i;

    invoke-virtual {v1, v0}, Lpmsj/work/d/i;->a(I)V

    :cond_0
    return-void
.end method

.method private j()I
    .locals 1

    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    if-nez v0, :cond_0

    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    goto :goto_0
.end method

.method private k()Ljava/util/Vector;
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/ad;->L:[Ljava/util/Vector;

    invoke-direct {p0}, Lpmsj/work/e/ad;->j()I

    move-result v1

    aget-object v0, v0, v1

    return-object v0
.end method

.method private n()Z
    .locals 2

    invoke-direct {p0}, Lpmsj/work/e/ad;->k()Ljava/util/Vector;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-nez v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    iget-object v1, p0, Lpmsj/work/e/ad;->M:Lpmsj/work/d/i;

    invoke-virtual {v1, v0}, Lpmsj/work/d/i;->d(I)Z

    move-result v0

    goto :goto_0
.end method

.method private o()V
    .locals 6

    const/4 v5, 0x1

    iget-object v0, p0, Lpmsj/work/e/ad;->K:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    invoke-direct {p0}, Lpmsj/work/e/ad;->j()I

    move-result v0

    invoke-direct {p0, v0}, Lpmsj/work/e/ad;->C(I)B

    move-result v0

    const/4 v1, -0x1

    if-ne v1, v0, :cond_1

    invoke-direct {p0}, Lpmsj/work/e/ad;->p()V

    :cond_0
    return-void

    :cond_1
    invoke-direct {p0}, Lpmsj/work/e/ad;->j()I

    move-result v1

    iget-object v2, p0, Lpmsj/work/e/ad;->P:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    if-ge v1, v2, :cond_0

    iget-object v1, p0, Lpmsj/work/e/ad;->P:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [La/c/i;

    if-eqz v0, :cond_0

    move v1, v5

    :goto_0
    array-length v2, v0

    if-ge v1, v2, :cond_0

    iget-byte v2, p0, Lpmsj/work/e/ad;->X:B

    if-ne v1, v2, :cond_2

    iget-object v2, p0, Lpmsj/work/e/ad;->K:Lpmsj/work/d/l;

    aget-object v3, v0, v1

    invoke-virtual {v3}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    :goto_1
    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_0

    :cond_2
    array-length v2, v0

    sub-int/2addr v2, v5

    if-ne v1, v2, :cond_3

    iget-object v2, p0, Lpmsj/work/e/ad;->K:Lpmsj/work/d/l;

    aget-object v3, v0, v1

    invoke-virtual {v3}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    goto :goto_1

    :cond_3
    iget-object v2, p0, Lpmsj/work/e/ad;->K:Lpmsj/work/d/l;

    aget-object v3, v0, v1

    invoke-virtual {v3}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v3

    iget-object v4, p0, Lpmsj/work/e/ad;->K:Lpmsj/work/d/l;

    iget v4, v4, Lpmsj/work/d/l;->k:I

    div-int/lit8 v4, v4, 0x3

    invoke-virtual {v2, v3, v4}, Lpmsj/work/d/l;->a(Ljava/lang/String;I)V

    goto :goto_1
.end method

.method private p()V
    .locals 3

    const/16 v0, 0x43b

    const/4 v1, 0x5

    iget-object v2, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v2}, Lpmsj/work/d/k;->f()I

    move-result v2

    int-to-byte v2, v2

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(IBB)V

    return-void
.end method

.method private q()V
    .locals 5

    const/4 v4, 0x0

    const/16 v0, 0x43b

    iget-object v1, p0, Lpmsj/work/e/ad;->M:Lpmsj/work/d/i;

    invoke-virtual {v1}, Lpmsj/work/d/i;->c()I

    move-result v1

    int-to-byte v1, v1

    iget-object v2, p0, Lpmsj/work/e/ad;->M:Lpmsj/work/d/i;

    invoke-virtual {v2}, Lpmsj/work/d/i;->d()I

    move-result v2

    int-to-byte v2, v2

    iget-object v3, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v3}, Lpmsj/work/d/k;->f()I

    move-result v3

    int-to-byte v3, v3

    invoke-static {v0, v4, v1, v2, v3}, Lpmsj/work/main/w;->a(IBBBB)V

    const/4 v0, 0x1

    invoke-static {v0, v4}, Lpmsj/work/main/t;->a(ZZ)V

    return-void
.end method


# virtual methods
.method public final Z()V
    .locals 2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "*5\u3010\u73a9\u5bb6\u6c42\u8d2d\u5355\u3011_*9\u5168\u670d\u6240\u6709\u9700\u8981\u8d2d\u5165\u4ed9\u6676\u7684\u8ba2\u5355(\u5305\u62ec\u81ea\u5df1\u7684\u6c42\u8d2d\u5355\uff0c\u4f46\u65e0\u6cd5\u4ea4\u6613\u81ea\u5df1\u7684\u8ba2\u5355)\u90fd\u663e\u793a\u5728\u6b64\u5904\uff0c\u60a8\u53ef\u4ee5\u5728\u6b64\u5904\u5e94\u5355\uff0c\u628a\u81ea\u5df1\u7684\u4ed9\u6676\u51fa\u552e\u7ed9\u8ba2\u5355\u53d1\u5e03\u8005\uff0c\u4ee5\u83b7\u53d6\u94f6\u4e24\u3002_*5\u3010\u73a9\u5bb6\u51fa\u552e\u5355\u3011_*9\u5168\u670d\u6240\u6709\u60f3\u8981\u5356\u51fa\u4ed9\u6676\u7684\u8ba2\u5355(\u5305\u62ec\u81ea\u5df1\u7684\u51fa\u552e\u5355\uff0c\u4f46\u65e0\u6cd5\u4ea4\u6613\u81ea\u5df1\u7684\u8ba2\u5355)\u90fd\u663e\u793a\u5728\u6b64\u5904\uff0c\u60a8\u53ef\u4ee5\u5728\u6b64\u5904\u5e94\u5355\uff0c\u7528\u94f6\u4e24\u8d2d\u4e70\u5230\u76f8\u5e94\u4ed9\u6676\u3002_*5\u3010\u8bf4\u660e\u3011_*9\u4e70\u5165\u9700\u652f\u4ed8\u7684\u4ed9\u6676/\u94f6\u4e24\uff0c\u76f4\u63a5\u4ece\u8d2d\u4e70\u8005\u7684\u80cc\u5305\u4e0a\u6263\u9664\uff1b\u5356\u51fa\u6240\u5f97\u7684\u4ed9\u6676/\u94f6\u4e24\uff0c\u5c06\u901a\u8fc7\u90ae\u4ef6\u7684\u65b9\u5f0f\u53d1\u9001\u7ed9\u51fa\u552e\u8005\u3002"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->b(Ljava/lang/String;)V

    return-void
.end method

.method public final a(Lpmsj/work/main/w;)V
    .locals 11

    const/4 v2, 0x3

    const/4 v3, 0x2

    const/4 v10, -0x1

    const/4 v5, 0x1

    const/4 v9, 0x0

    invoke-virtual {p1, v9}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    invoke-static {v9, v9}, Lpmsj/work/main/t;->a(ZZ)V

    :cond_1
    return-void

    :pswitch_1
    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    new-array v1, v0, [Ljava/lang/String;

    move v2, v9

    :goto_1
    if-ge v2, v0, :cond_2

    add-int/lit8 v4, v3, 0x1

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v1, v2

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    move v3, v4

    goto :goto_1

    :cond_2
    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->a([Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    iget-object v2, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    array-length v1, v1

    div-int v1, v2, v1

    iget-object v2, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    iget v2, v2, Lpmsj/work/d/b;->l:I

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/k;->h(II)V

    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->i()V

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a(Lpmsj/work/d/k;)V

    move v0, v9

    :goto_2
    iget-object v1, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v1}, Lpmsj/work/d/k;->h()I

    move-result v1

    if-ge v0, v1, :cond_3

    add-int/lit8 v1, v0, 0xa

    iget-object v2, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {p0, v1, v2}, Lpmsj/work/e/ad;->a(ILpmsj/work/d/b;)V

    add-int/lit8 v0, v0, 0x1

    goto :goto_2

    :cond_3
    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    if-nez v0, :cond_4

    move v0, v5

    :goto_3
    new-array v1, v0, [Ljava/util/Vector;

    iput-object v1, p0, Lpmsj/work/e/ad;->L:[Ljava/util/Vector;

    move v1, v9

    :goto_4
    iget-object v2, p0, Lpmsj/work/e/ad;->L:[Ljava/util/Vector;

    array-length v2, v2

    if-ge v1, v2, :cond_5

    iget-object v2, p0, Lpmsj/work/e/ad;->L:[Ljava/util/Vector;

    new-instance v4, Ljava/util/Vector;

    invoke-direct {v4}, Ljava/util/Vector;-><init>()V

    aput-object v4, v2, v1

    add-int/lit8 v1, v1, 0x1

    goto :goto_4

    :cond_4
    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->h()I

    move-result v0

    goto :goto_3

    :cond_5
    new-array v1, v0, [Z

    iput-object v1, p0, Lpmsj/work/e/ad;->O:[Z

    new-array v0, v0, [I

    iput-object v0, p0, Lpmsj/work/e/ad;->N:[I

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Lpmsj/work/e/ad;->d(Ljava/lang/String;)V

    goto :goto_0

    :pswitch_2
    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    if-lez v1, :cond_1

    new-array v2, v1, [La/c/i;

    move v3, v9

    :goto_5
    if-ge v3, v1, :cond_6

    iget-object v0, p1, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v4, v3, 0x2

    invoke-virtual {v0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v2, v3

    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_5

    :cond_6
    iget-byte v0, p0, Lpmsj/work/e/ad;->W:B

    aget-object v0, v2, v0

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    invoke-direct {p0, v0}, Lpmsj/work/e/ad;->C(I)B

    move-result v0

    if-ne v10, v0, :cond_7

    iget-object v0, p0, Lpmsj/work/e/ad;->P:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_7
    invoke-direct {p0}, Lpmsj/work/e/ad;->o()V

    goto/16 :goto_0

    :pswitch_3
    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    iget-object v3, p0, Lpmsj/work/e/ad;->O:[Z

    aput-boolean v5, v3, v2

    if-lez v1, :cond_b

    iget-object v3, p1, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    const/4 v4, 0x4

    sub-int/2addr v3, v4

    div-int/2addr v3, v1

    :goto_6
    iget-object v4, p0, Lpmsj/work/e/ad;->L:[Ljava/util/Vector;

    aget-object v4, v4, v2

    invoke-direct {p0}, Lpmsj/work/e/ad;->j()I

    move-result v5

    move v6, v9

    :goto_7
    if-ge v6, v1, :cond_9

    mul-int v7, v6, v3

    add-int/lit8 v7, v7, 0x4

    invoke-virtual {p1, v3, v7}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v7

    invoke-virtual {v7, v9}, La/c/a;->a(I)I

    move-result v8

    invoke-static {v8, v4}, Lpmsj/work/e/ad;->a(ILjava/util/Vector;)I

    move-result v8

    if-ne v10, v8, :cond_8

    invoke-virtual {v4, v7}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    if-ne v5, v2, :cond_8

    invoke-direct {p0, v7}, Lpmsj/work/e/ad;->a(La/c/a;)V

    :cond_8
    add-int/lit8 v6, v6, 0x1

    goto :goto_7

    :cond_9
    iget-object v1, p0, Lpmsj/work/e/ad;->N:[I

    aput v0, v1, v2

    invoke-direct {p0}, Lpmsj/work/e/ad;->i()V

    goto/16 :goto_0

    :pswitch_4
    invoke-virtual {p1, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/ad;->L:[Ljava/util/Vector;

    aget-object v1, v1, v0

    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    invoke-static {v2, v1}, Lpmsj/work/e/ad;->a(ILjava/util/Vector;)I

    move-result v2

    if-eq v10, v2, :cond_0

    invoke-virtual {v1, v2}, Ljava/util/Vector;->removeElementAt(I)V

    invoke-direct {p0}, Lpmsj/work/e/ad;->j()I

    move-result v1

    iget-object v2, p0, Lpmsj/work/e/ad;->N:[I

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->b(I)S

    move-result v3

    aput v3, v2, v1

    if-ne v0, v1, :cond_a

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    invoke-virtual {p0}, Lpmsj/work/e/ad;->ag()V

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->i()V

    :cond_a
    invoke-direct {p0}, Lpmsj/work/e/ad;->n()Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/ad;->q()V

    goto/16 :goto_0

    :cond_b
    move v3, v9

    goto :goto_6

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_3
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_4
    .end packed-switch
.end method

.method public final ag()V
    .locals 3

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    invoke-direct {p0}, Lpmsj/work/e/ad;->k()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v0

    if-gtz v0, :cond_0

    :goto_0
    return-void

    :cond_0
    const/4 v0, 0x0

    move v2, v0

    :goto_1
    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v2, v0, :cond_1

    invoke-virtual {v1, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-direct {p0, v0}, Lpmsj/work/e/ad;->a(La/c/a;)V

    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_1

    :cond_1
    invoke-direct {p0}, Lpmsj/work/e/ad;->i()V

    goto :goto_0
.end method

.method protected final b(Lpmsj/work/d/b;)V
    .locals 4

    const/4 v3, 0x0

    const/4 v2, 0x1

    iget v0, p1, Lpmsj/work/d/b;->g:I

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-direct {p0}, Lpmsj/work/e/ad;->i()V

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->k()V

    invoke-direct {p0}, Lpmsj/work/e/ad;->n()Z

    move-result v0

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/e/ad;->O:[Z

    iget-object v1, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v1}, Lpmsj/work/d/k;->f()I

    move-result v1

    aget-boolean v0, v0, v1

    if-nez v0, :cond_1

    invoke-direct {p0}, Lpmsj/work/e/ad;->q()V

    :goto_1
    invoke-direct {p0}, Lpmsj/work/e/ad;->o()V

    goto :goto_0

    :cond_1
    invoke-virtual {p0}, Lpmsj/work/e/ad;->ag()V

    goto :goto_1

    :pswitch_2
    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->h()I

    move-result v0

    invoke-direct {p0}, Lpmsj/work/e/ad;->k()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    if-ge v0, v1, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/ad;->k()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    if-nez v0, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-array v1, v2, [Ljava/lang/String;

    const-string v2, "\u51fa\u552e"

    aput-object v2, v1, v3

    invoke-virtual {v0, v1, p0}, Lpmsj/work/d/n;->a([Ljava/lang/String;Lpmsj/work/d/c;)V

    goto :goto_0

    :cond_2
    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v0

    if-ne v0, v2, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-array v1, v2, [Ljava/lang/String;

    const-string v2, "\u8d2d\u4e70"

    aput-object v2, v1, v3

    invoke-virtual {v0, v1, p0}, Lpmsj/work/d/n;->a([Ljava/lang/String;Lpmsj/work/d/c;)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x4e9d1
        :pswitch_1
        :pswitch_0
        :pswitch_2
    .end packed-switch
.end method

.method public final b(Ljava/lang/String;)Z
    .locals 10

    const/4 v8, 0x3

    const/4 v5, 0x1

    const-string v9, "\u4e2a"

    const-string v7, "*2"

    const-string v6, "*0"

    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->f()I

    move-result v1

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->h()I

    move-result v0

    iget-object v2, p0, Lpmsj/work/e/ad;->L:[Ljava/util/Vector;

    aget-object v2, v2, v1

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v3

    if-lt v0, v3, :cond_0

    move v0, v5

    :goto_0
    return v0

    :cond_0
    invoke-virtual {v2, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    new-instance v2, Ljava/lang/StringBuffer;

    invoke-direct {v2}, Ljava/lang/StringBuffer;-><init>()V

    invoke-virtual {v0, v5}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v3

    const-string v4, "\u51fa\u552e"

    invoke-virtual {p1, v4}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v4

    if-eqz v4, :cond_2

    if-nez v1, :cond_2

    const-string v1, "\u60a8\u786e\u5b9a\u8981"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\u51fa\u552e"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "*2"

    invoke-virtual {v2, v7}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v2, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "*0"

    invoke-virtual {v2, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\u4e2a"

    invoke-virtual {v2, v9}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\u4ed9\u6676"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\u6362\u53d6"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "*2"

    invoke-virtual {v2, v7}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0, v8}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "*0"

    invoke-virtual {v2, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u94f6\u4e24"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\uff1f"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v2}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x0

    invoke-virtual {v0, v1, v2, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    :cond_1
    :goto_1
    move v0, v5

    goto :goto_0

    :cond_2
    const-string v3, "\u8d2d\u4e70"

    invoke-virtual {p1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_1

    if-ne v1, v5, :cond_1

    const-string v1, "\u60a8\u786e\u5b9a\u82b1"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "*2"

    invoke-virtual {v2, v7}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0, v8}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "*0"

    invoke-virtual {v2, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\u94f6\u4e24"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\u8d2d\u4e70"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "*2"

    invoke-virtual {v2, v7}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0, v5}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "*0"

    invoke-virtual {v2, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u4e2a"

    invoke-virtual {v2, v9}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u4ed9\u6676"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\uff1f"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v2}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1, v5, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto :goto_1
.end method

.method protected final c()V
    .locals 3

    const v0, 0x4e9d2

    invoke-virtual {p0, v0}, Lpmsj/work/e/ad;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/ad;->K:Lpmsj/work/d/l;

    const v0, 0x4e9d4

    invoke-virtual {p0, v0}, Lpmsj/work/e/ad;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a(Z)V

    const v1, 0x4e9d3

    invoke-virtual {p0, v1}, Lpmsj/work/e/ad;->w(I)Lpmsj/work/d/b;

    move-result-object v1

    check-cast v1, Lpmsj/work/d/l;

    iput-object v1, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    iget-object v2, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/b;->l:I

    iget v0, v0, Lpmsj/work/d/b;->l:I

    add-int/2addr v0, v2

    const/16 v2, 0xa

    sub-int/2addr v0, v2

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->j(I)V

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    const/16 v1, 0x403

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->l(I)V

    const v0, 0x4e9d1

    invoke-virtual {p0, v0}, Lpmsj/work/e/ad;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/k;

    iput-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    iget-object v0, p0, Lpmsj/work/e/ad;->e:Lpmsj/work/d/k;

    const v1, 0x880010

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->l(I)V

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->g()Lpmsj/work/d/i;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/e/ad;->M:Lpmsj/work/d/i;

    invoke-virtual {p0}, Lpmsj/work/e/ad;->P()V

    return-void
.end method

.method public final c_(I)V
    .locals 5

    const/4 v4, 0x1

    const/4 v3, 0x0

    invoke-direct {p0}, Lpmsj/work/e/ad;->k()Ljava/util/Vector;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v1}, Lpmsj/work/d/l;->h()I

    move-result v1

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v2

    if-lt v1, v2, :cond_1

    const/4 v0, 0x0

    :goto_0
    if-nez v0, :cond_2

    :cond_0
    :goto_1
    return-void

    :cond_1
    iget-object v1, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    invoke-virtual {v1}, Lpmsj/work/d/l;->h()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/a;

    move-object v0, p0

    goto :goto_0

    :cond_2
    if-eqz p1, :cond_3

    if-ne v4, p1, :cond_0

    :cond_3
    const/16 v1, 0x43b

    const/4 v2, 0x3

    invoke-virtual {v0, v3}, La/c/a;->a(I)I

    move-result v0

    invoke-static {v1, v2, v0}, Lpmsj/work/main/w;->a(IBI)V

    invoke-static {v4, v3}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_1
.end method

.method protected final e(Lpmsj/work/d/b;)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/e/ad;->f:Lpmsj/work/d/l;

    if-ne v0, p1, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/ad;->n()Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/ad;->q()V

    :cond_0
    return-void
.end method

.method public final y(I)V
    .locals 3

    invoke-super {p0, p1}, Lpmsj/work/d/c;->y(I)V

    const/16 v0, 0x43b

    const/4 v1, 0x4

    invoke-virtual {p0}, Lpmsj/work/e/ad;->af()I

    move-result v2

    int-to-byte v2, v2

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(IBB)V

    invoke-direct {p0}, Lpmsj/work/e/ad;->p()V

    invoke-direct {p0}, Lpmsj/work/e/ad;->q()V

    return-void
.end method
